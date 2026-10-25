"""
Capa de Infraestructura: Repositorio SQLite para Reto Fit 2026
Criterios EARS: AC-3.1 a AC-3.6
"""
import os
import json
import sqlite3
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from src.domain.participant import Participant
from src.domain.activity import DailyActivity


class SQLiteChallengeRepository:
    """Implementacion de persistencia en SQLite para participantes, pagos y actividades."""

    def __init__(self, db_path: str = "data/retofit.db") -> None:
        self.db_path = db_path
        dir_name = os.path.dirname(self.db_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        """Crea automaticamente el esquema de tablas si no existe."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS participants (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    participant_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    participant_id TEXT NOT NULL,
                    week_number INTEGER NOT NULL,
                    day_of_week INTEGER NOT NULL,
                    calories INTEGER NOT NULL,
                    steps INTEGER NOT NULL,
                    is_successful INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(participant_id, week_number, day_of_week),
                    FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS weekly_closes (
                    week_number INTEGER PRIMARY KEY,
                    compliant_participants TEXT NOT NULL,
                    non_compliant_participants TEXT NOT NULL,
                    pool_collected REAL NOT NULL,
                    rollover_amount REAL NOT NULL,
                    payout_per_compliant REAL NOT NULL,
                    closed_at TEXT NOT NULL
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS rollover_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    current_rollover REAL NOT NULL
                );
                """
            )
            # Inicializar rollover en 0 si no existe
            cursor.execute(
                """
                INSERT OR IGNORE INTO rollover_state (id, current_rollover)
                VALUES (1, 0.0);
                """
            )
            conn.commit()

    def save_participant(self, participant: Participant) -> None:
        """Persiste un participante en la base de datos."""
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO participants (id, name, created_at) VALUES (?, ?, ?);",
                (participant.id, participant.name, now),
            )
            conn.commit()

    def get_participant(self, participant_id: str) -> Optional[Participant]:
        """Obtiene un participante reconstruido con sus pagos."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT id, name FROM participants WHERE id = ?;", (participant_id,)
            ).fetchone()
            if not row:
                return None
            p = Participant(id=row["id"], name=row["name"])
            payments = conn.execute(
                "SELECT amount FROM payments WHERE participant_id = ? ORDER BY id ASC;",
                (participant_id,),
            ).fetchall()
            for pay in payments:
                p.add_contribution(pay["amount"])
            return p

    def list_participants(self) -> List[Participant]:
        """Lista todos los participantes registrados con sus pagos."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT id, name FROM participants ORDER BY created_at ASC;").fetchall()
            participants: List[Participant] = []
            for r in rows:
                p = Participant(id=r["id"], name=r["name"])
                payments = conn.execute(
                    "SELECT amount FROM payments WHERE participant_id = ? ORDER BY id ASC;",
                    (r["id"],),
                ).fetchall()
                for pay in payments:
                    p.add_contribution(pay["amount"])
                participants.append(p)
            return participants

    def record_payment(self, participant_id: str, amount: float) -> None:
        """Registra un abono para un participante."""
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO payments (participant_id, amount, created_at) VALUES (?, ?, ?);",
                (participant_id, amount, now),
            )
            conn.commit()

    def record_activity(
        self,
        participant_id: str,
        week_number: int,
        day_of_week: int,
        activity: DailyActivity,
    ) -> None:
        """Registra la actividad diaria de un participante."""
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO activities (participant_id, week_number, day_of_week, calories, steps, is_successful, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(participant_id, week_number, day_of_week) DO UPDATE SET
                    calories=excluded.calories,
                    steps=excluded.steps,
                    is_successful=excluded.is_successful,
                    created_at=excluded.created_at;
                """,
                (
                    participant_id,
                    week_number,
                    day_of_week,
                    activity.calories,
                    activity.steps,
                    1 if activity.is_successful() else 0,
                    now,
                ),
            )
            conn.commit()

    def record_week_close(
        self,
        week_number: int,
        compliant_ids: List[str],
        non_compliant_ids: List[str],
        pool_collected: float,
        rollover_amount: float,
        payout_per_compliant: float,
    ) -> None:
        """Registra la liquidacion y cierre de una semana."""
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO weekly_closes 
                (week_number, compliant_participants, non_compliant_participants, pool_collected, rollover_amount, payout_per_compliant, closed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    week_number,
                    json.dumps(compliant_ids),
                    json.dumps(non_compliant_ids),
                    pool_collected,
                    rollover_amount,
                    payout_per_compliant,
                    now,
                ),
            )
            conn.execute(
                "UPDATE rollover_state SET current_rollover = ? WHERE id = 1;",
                (rollover_amount,),
            )
            conn.commit()

    def get_rollover(self) -> float:
        """Obtiene el fondo acumulado de rollover actual."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT current_rollover FROM rollover_state WHERE id = 1;").fetchone()
            return float(row["current_rollover"]) if row else 0.0

    def set_rollover(self, amount: float) -> None:
        """Actualiza el fondo acumulado de rollover."""
        with self._get_connection() as conn:
            conn.execute("UPDATE rollover_state SET current_rollover = ? WHERE id = 1;", (amount,))
            conn.commit()

    def load_all_state(self) -> Dict[str, Any]:
        """Carga todo el estado estructurado para rehidratar el servicio."""
        with self._get_connection() as conn:
            participants = self.list_participants()

            activities_rows = conn.execute(
                "SELECT participant_id, week_number, day_of_week, calories, steps FROM activities;"
            ).fetchall()

            activities_by_participant: Dict[str, List[Dict[str, Any]]] = {}
            for row in activities_rows:
                pid = row["participant_id"]
                if pid not in activities_by_participant:
                    activities_by_participant[pid] = []
                activities_by_participant[pid].append(
                    {
                        "week_number": row["week_number"],
                        "day_of_week": row["day_of_week"],
                        "calories": row["calories"],
                        "steps": row["steps"],
                    }
                )

            closes_rows = conn.execute(
                "SELECT week_number, compliant_participants, non_compliant_participants, pool_collected, rollover_amount, payout_per_compliant FROM weekly_closes ORDER BY week_number ASC;"
            ).fetchall()
            weekly_closes: List[Dict[str, Any]] = [
                {
                    "week_number": r["week_number"],
                    "compliant_participants": json.loads(r["compliant_participants"]),
                    "non_compliant_participants": json.loads(r["non_compliant_participants"]),
                    "pool_collected": r["pool_collected"],
                    "rollover_amount": r["rollover_amount"],
                    "payout_per_compliant": r["payout_per_compliant"],
                }
                for r in closes_rows
            ]

            rollover = self.get_rollover()

            return {
                "participants": participants,
                "activities": activities_by_participant,
                "weekly_closes": weekly_closes,
                "rollover": rollover,
            }

    def update_participant_name(self, participant_id: str, new_name: str) -> None:
        """Actualiza el nombre de un participante registrado."""
        with self._get_connection() as conn:
            conn.execute("UPDATE participants SET name = ? WHERE id = ?;", (new_name, participant_id))
            conn.commit()

    def delete_participant(self, participant_id: str) -> bool:
        """Elimina un participante y sus registros asociados por clave foranea en cascada."""
        with self._get_connection() as conn:
            cur = conn.execute("DELETE FROM participants WHERE id = ?;", (participant_id,))
            conn.commit()
            return cur.rowcount > 0

    def delete_last_payment(self, participant_id: str) -> Optional[float]:
        """Elimina el abono mas reciente de un participante y retorna el monto eliminado."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT id, amount FROM payments WHERE participant_id = ? ORDER BY id DESC LIMIT 1;",
                (participant_id,),
            ).fetchone()
            if not row:
                return None
            pay_id = row["id"]
            amount = float(row["amount"])
            conn.execute("DELETE FROM payments WHERE id = ?;", (pay_id,))
            conn.commit()
            return amount

    def delete_activity(self, participant_id: str, week_number: int, day_of_week: int) -> bool:
        """Elimina el registro de actividad de un dia especifico."""
        with self._get_connection() as conn:
            cur = conn.execute(
                "DELETE FROM activities WHERE participant_id = ? AND week_number = ? AND day_of_week = ?;",
                (participant_id, week_number, day_of_week),
            )
            conn.commit()
            return cur.rowcount > 0

