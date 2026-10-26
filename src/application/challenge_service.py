"""
Capa de Aplicacion: Servicio Orquestador del Reto Fit
Criterios EARS: AC-1.1 a AC-1.8
"""
from typing import Dict, List, Optional, Set, Any
from src.domain.activity import DailyActivity
from src.domain.challenge_week import ChallengeWeek
from src.domain.challenge_pool import WeeklyPool
from src.domain.participant import Participant
from src.domain.financial_summary import FinancialSummary
from src.domain.weekly_report import get_expected_contribution_for_week
from src.application.dto import (
    RegisterParticipantDTO,
    RecordPaymentDTO,
    RecordActivityDTO,
    WeeklyCloseResultDTO,
    ParticipantSummaryDTO,
    GeneralSummaryDTO,
    WeeklyParticipantReportDTO,
    WeeklyReportDTO,
    ParticipantRankingDTO,
    WeeklyStatsTrendDTO,
    GlobalStatsDTO,
)
from src.domain.challenge_stats import calculate_global_stats
from src.application.repository import ChallengeRepository


class ChallengeService:
    def __init__(self, repository: Optional[ChallengeRepository] = None) -> None:
        self.repository = repository
        self.participants: Dict[str, Participant] = {}
        self.weeks: Dict[int, ChallengeWeek] = {}
        self.pools: Dict[int, WeeklyPool] = {}
        self.accumulated_earnings: Dict[str, float] = {}
        self.participant_met_weeks: Dict[str, int] = {}
        self.participant_missed_weeks: Dict[str, int] = {}
        self.current_rollover: float = 0.0
        self.closed_weeks: Set[int] = set()
        self.closed_weeks_data: Dict[int, Dict[str, Any]] = {}

        if self.repository is not None:
            self._rehydrate()

    def _rehydrate(self) -> None:
        """Restaura el estado completo desde el repositorio de persistencia."""
        if self.repository is None:
            return
        state = self.repository.load_all_state()

        # 1. Participantes y sus pagos
        for p in state.get("participants", []):
            self.participants[p.id] = p
            self.accumulated_earnings[p.id] = 0.0
            self.participant_met_weeks[p.id] = 0
            self.participant_missed_weeks[p.id] = 0

        # 2. Actividades diarias
        activities_map = state.get("activities", {})
        for p_id, act_list in activities_map.items():
            if p_id in self.participants:
                for a in act_list:
                    act_obj = DailyActivity(calories=a["calories"], steps=a["steps"])
                    self.participants[p_id].record_activity(
                        week_number=a["week_number"],
                        day_of_week=a["day_of_week"],
                        activity=act_obj,
                    )

        # 3. Cierres semanales acumulados
        for close in state.get("weekly_closes", []):
            wn = close["week_number"]
            self.closed_weeks.add(wn)
            self.closed_weeks_data[wn] = close
            payout = close["payout_per_compliant"]
            for cid in close["compliant_participants"]:
                if cid in self.accumulated_earnings:
                    self.accumulated_earnings[cid] = round(self.accumulated_earnings[cid] + payout, 2)
                if cid in self.participant_met_weeks:
                    self.participant_met_weeks[cid] += 1
            for nid in close["non_compliant_participants"]:
                if nid in self.participant_missed_weeks:
                    self.participant_missed_weeks[nid] += 1

        # 4. Rollover
        self.current_rollover = float(state.get("rollover", 0.0))

    def register_participant(self, dto: RegisterParticipantDTO) -> Participant:
        """Registra un nuevo participante en el sistema."""
        if dto.id in self.participants:
            raise ValueError(f"Participante con ID {dto.id} ya existe")
        p = Participant(id=dto.id, name=dto.name)
        self.participants[dto.id] = p
        self.accumulated_earnings[dto.id] = 0.0
        self.participant_met_weeks[dto.id] = 0
        self.participant_missed_weeks[dto.id] = 0
        if self.repository is not None:
            self.repository.save_participant(p)
        return p

    def record_payment(self, dto: RecordPaymentDTO) -> float:
        """Registra una aportacion economica para un participante."""
        if dto.participant_id not in self.participants:
            raise KeyError(f"Participante {dto.participant_id} no encontrado")
        participant = self.participants[dto.participant_id]
        participant.add_contribution(dto.amount)
        if self.repository is not None:
            self.repository.record_payment(dto.participant_id, dto.amount)
        return participant.total_contributed

    def record_daily_activity(self, dto: RecordActivityDTO) -> bool:
        """Registra la actividad diaria de un participante."""
        if dto.participant_id not in self.participants:
            raise KeyError(f"Participante {dto.participant_id} no encontrado")
        activity = DailyActivity(calories=dto.calories, steps=dto.steps)
        participant = self.participants[dto.participant_id]
        participant.record_activity(
            week_number=dto.week_number,
            day_of_week=dto.day_of_week,
            activity=activity,
        )
        if self.repository is not None:
            self.repository.record_activity(
                participant_id=dto.participant_id,
                week_number=dto.week_number,
                day_of_week=dto.day_of_week,
                activity=activity,
            )
        return activity.is_successful()

    def update_participant_name(self, participant_id: str, new_name: str) -> Participant:
        """Actualiza el nombre de un participante registrado."""
        if participant_id not in self.participants:
            raise KeyError(f"Participante {participant_id} no encontrado")
        participant = self.participants[participant_id]
        participant.update_name(new_name)
        if self.repository is not None:
            self.repository.update_participant_name(participant_id, participant.name)
        return participant

    def delete_participant(self, participant_id: str) -> bool:
        """Elimina un participante y sus registros asociados."""
        if participant_id not in self.participants:
            raise KeyError(f"Participante {participant_id} no encontrado")
        del self.participants[participant_id]
        self.accumulated_earnings.pop(participant_id, None)
        self.participant_met_weeks.pop(participant_id, None)
        self.participant_missed_weeks.pop(participant_id, None)
        if self.repository is not None:
            self.repository.delete_participant(participant_id)
        return True

    def delete_last_payment(self, participant_id: str) -> float:
        """Elimina el abono mas reciente de un participante y retorna el monto."""
        if participant_id not in self.participants:
            raise KeyError(f"Participante {participant_id} no encontrado")
        participant = self.participants[participant_id]
        removed = participant.remove_last_contribution()
        if self.repository is not None:
            self.repository.delete_last_payment(participant_id)
        return removed

    def delete_daily_activity(self, participant_id: str, week_number: int, day_of_week: int) -> bool:
        """Elimina la actividad registrada para un dia y semana especificos."""
        if participant_id not in self.participants:
            raise KeyError(f"Participante {participant_id} no encontrado")
        participant = self.participants[participant_id]
        removed = participant.remove_activity(week_number, day_of_week)
        if self.repository is not None:
            self.repository.delete_activity(participant_id, week_number, day_of_week)
        return removed

    def close_and_liquidate_week(self, week_number: int) -> WeeklyCloseResultDTO:
        """Evalua el cumplimiento semanal de todos los participantes,
        cobra penalizaciones de $100 a los incumplidores y distribuye la bolsa
        (o traslada rollover a la siguiente semana).
        """
        week = ChallengeWeek(week_number=week_number)
        pool = WeeklyPool(week_number=week_number, initial_rollover=self.current_rollover)

        for p_id, participant in self.participants.items():
            successful_days = participant.get_successful_days(week_number)
            is_met = week.register_result(p_id, successful_days)
            if is_met:
                self.participant_met_weeks[p_id] += 1
            else:
                self.participant_missed_weeks[p_id] += 1
                pool.add_penalty(100.0)

        met_count = len(week.met_participants)
        missed_count = len(week.missed_participants)

        gain_per_person, rollover = pool.distribute(met_participants_count=met_count)

        if met_count > 0:
            for p_id in week.met_participants:
                self.accumulated_earnings[p_id] = round(
                    self.accumulated_earnings[p_id] + gain_per_person, 2
                )

        self.current_rollover = rollover
        self.weeks[week_number] = week
        self.pools[week_number] = pool
        self.closed_weeks.add(week_number)
        self.closed_weeks_data[week_number] = {
            "week_number": week_number,
            "compliant_participants": list(week.met_participants),
            "non_compliant_participants": list(week.missed_participants),
            "pool_collected": pool.current_total,
            "rollover_amount": rollover,
            "payout_per_compliant": gain_per_person,
        }

        if self.repository is not None:
            self.repository.record_week_close(
                week_number=week_number,
                compliant_ids=list(week.met_participants),
                non_compliant_ids=list(week.missed_participants),
                pool_collected=pool.current_total,
                rollover_amount=rollover,
                payout_per_compliant=gain_per_person,
            )

        return WeeklyCloseResultDTO(
            week_number=week_number,
            met_count=met_count,
            missed_count=missed_count,
            pool_collected=pool.current_total,
            gain_per_participant=gain_per_person,
            rollover_to_next=rollover,
        )

    def get_participant_summary(self, participant_id: str) -> ParticipantSummaryDTO:
        """Genera el concentrado y balance financiero de un participante."""
        if participant_id not in self.participants:
            raise KeyError(f"Participante {participant_id} no encontrado")
        p = self.participants[participant_id]
        fin = FinancialSummary.calculate(
            participant_id=p.id,
            name=p.name,
            total_contributed=p.total_contributed,
            weeks_met=self.participant_met_weeks[p.id],
            weeks_missed=self.participant_missed_weeks[p.id],
            total_earnings=self.accumulated_earnings[p.id],
        )
        return ParticipantSummaryDTO(
            participant_id=fin.participant_id,
            name=fin.name,
            total_contributed=fin.total_contributed,
            weeks_met=fin.weeks_met,
            weeks_missed=fin.weeks_missed,
            total_penalties=fin.total_penalties,
            total_earnings=fin.total_earnings,
            net_balance=fin.net_balance,
        )

    def get_general_summary(self) -> GeneralSummaryDTO:
        """Genera el concentrado general del evento Reto Fit."""
        part_summaries: List[ParticipantSummaryDTO] = [
            self.get_participant_summary(p_id) for p_id in self.participants
        ]
        total_funds = round(sum(p.total_contributed for p in part_summaries), 2)
        total_penalties = round(sum(p.total_penalties for p in part_summaries), 2)

        return GeneralSummaryDTO(
            total_participants=len(part_summaries),
            total_funds_collected=total_funds,
            total_penalties_distributed=total_penalties,
            total_rollover_balance=self.current_rollover,
            participants=part_summaries,
        )

    def get_weekly_report(self, week_number: int) -> WeeklyReportDTO:
        """Genera el informe semanal de cuotas acumuladas y cumplimiento fisico."""
        if week_number < 1 or week_number > 9:
            raise ValueError("El numero de semana debe estar entre 1 y 9")

        is_closed = week_number in self.weeks or week_number in self.closed_weeks
        gain_per_compliant = 0.0
        pool_amount = 0.0

        if is_closed and week_number in self.pools:
            pool = self.pools[week_number]
            pool_amount = pool.current_total
            met_count_closed = len(self.weeks[week_number].met_participants)
            if met_count_closed > 0:
                gain_per_compliant = round(pool_amount / met_count_closed, 2)
        elif is_closed and week_number in self.closed_weeks_data:
            cdata = self.closed_weeks_data[week_number]
            pool_amount = float(cdata.get("pool_collected", 0.0))
            gain_per_compliant = float(cdata.get("payout_per_compliant", 0.0))

        expected_per_part = get_expected_contribution_for_week(week_number)
        items: List[WeeklyParticipantReportDTO] = []
        met_count = 0
        missed_count = 0
        up_to_date_count = 0
        behind_count = 0

        for p_id, p in self.participants.items():
            days = p.get_successful_days(week_number)
            is_met = days >= 4
            if is_met:
                met_count += 1
            else:
                missed_count += 1

            if p.total_contributed >= expected_per_part:
                up_to_date_count += 1
                fin_status = "AL_CORRIENTE"
                pending = 0.0
            else:
                behind_count += 1
                fin_status = "PENDIENTE"
                pending = round(expected_per_part - p.total_contributed, 2)

            penalty = 0.0 if is_met else 100.0
            earnings = gain_per_compliant if (is_closed and is_met) else 0.0
            net_impact = round(earnings - penalty, 2)

            items.append(
                WeeklyParticipantReportDTO(
                    participant_id=p.id,
                    name=p.name,
                    successful_days=days,
                    is_met=is_met,
                    total_contributed=p.total_contributed,
                    expected_contribution=expected_per_part,
                    financial_status=fin_status,
                    pending_amount=pending,
                    penalty=penalty,
                    earnings=earnings,
                    net_balance_impact=net_impact,
                )
            )

        if not is_closed:
            pool_amount = round((missed_count * 100.0) + self.current_rollover, 2)
            gain_per_compliant = round(pool_amount / met_count, 2) if met_count > 0 else 0.0

        total_parts = len(items)
        rate = round((met_count / total_parts * 100), 1) if total_parts > 0 else 0.0
        total_exp = round(expected_per_part * total_parts, 2)
        total_col = round(sum(i.total_contributed for i in items), 2)

        return WeeklyReportDTO(
            week_number=week_number,
            total_participants=total_parts,
            met_count=met_count,
            missed_count=missed_count,
            compliance_rate=rate,
            expected_contribution_per_participant=expected_per_part,
            total_expected_funds=total_exp,
            total_collected_funds=total_col,
            participants_up_to_date=up_to_date_count,
            participants_behind=behind_count,
            is_closed=is_closed,
            pool_amount=pool_amount,
            gain_per_compliant=gain_per_compliant,
            participants=items,
        )

    def get_global_statistics(self) -> GlobalStatsDTO:
        """Genera las estadisticas globales, ranking de participantes y tendencias del reto."""
        participants_data = []
        for p in self.participants.values():
            activities_list = []
            for week_acts in p.activities.values():
                for act in week_acts.values():
                    activities_list.append({
                        "calories": act.calories,
                        "steps": act.steps,
                        "is_successful": act.is_successful(),
                    })
            participants_data.append({
                "participant_id": p.id,
                "name": p.name,
                "activities": activities_list,
            })

        total_parts = len(self.participants)
        weekly_raw_data = {}
        for w in range(1, 10):
            w_succ = sum(p.get_successful_days(w) for p in self.participants.values())
            w_compliant = sum(1 for p in self.participants.values() if p.get_successful_days(w) >= 4)
            w_missed = total_parts - w_compliant
            if w in self.closed_weeks_data:
                w_pool = float(self.closed_weeks_data[w].get("pool_collected", 0.0))
            elif w in self.pools:
                w_pool = float(self.pools[w].current_total)
            else:
                w_pool = float(w_missed * 100.0) if total_parts > 0 else 0.0
            weekly_raw_data[w] = {
                "successful_days": w_succ,
                "compliant": w_compliant,
                "total": total_parts,
                "pool": w_pool,
            }

        gen_summary = self.get_general_summary()
        total_penalties = gen_summary.total_penalties_distributed
        total_distributed_pool = sum(self.accumulated_earnings.values())

        domain_stats = calculate_global_stats(
            participants_data=participants_data,
            total_penalties=total_penalties,
            total_distributed_pool=total_distributed_pool,
            weekly_raw_data=weekly_raw_data,
            total_participants_count=total_parts,
        )

        return GlobalStatsDTO(
            total_calories=domain_stats.total_calories,
            total_steps=domain_stats.total_steps,
            total_successful_days=domain_stats.total_successful_days,
            total_activity_days=domain_stats.total_activity_days,
            average_daily_calories=domain_stats.average_daily_calories,
            average_daily_steps=domain_stats.average_daily_steps,
            total_participants=domain_stats.total_participants,
            total_penalties=domain_stats.total_penalties,
            total_distributed_pool=domain_stats.total_distributed_pool,
            ranking=[
                ParticipantRankingDTO(
                    rank_position=r.rank_position,
                    participant_id=r.participant_id,
                    name=r.name,
                    successful_days=r.successful_days,
                    total_calories=r.total_calories,
                    total_steps=r.total_steps,
                    is_podium=r.is_podium,
                )
                for r in domain_stats.ranking
            ],
            weekly_trends=[
                WeeklyStatsTrendDTO(
                    week_number=t.week_number,
                    successful_days=t.successful_days,
                    compliant_participants=t.compliant_participants,
                    total_participants=t.total_participants,
                    compliance_rate=t.compliance_rate,
                    pool_amount=t.pool_amount,
                )
                for t in domain_stats.weekly_trends
            ],
        )
