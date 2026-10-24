"""
Capa de Aplicacion: Servicio Orquestador del Reto Fit
Criterios EARS: AC-1.1 a AC-1.8
"""
from typing import Dict, List
from src.domain.activity import DailyActivity
from src.domain.challenge_week import ChallengeWeek
from src.domain.challenge_pool import WeeklyPool
from src.domain.participant import Participant
from src.domain.financial_summary import FinancialSummary
from src.application.dto import (
    RegisterParticipantDTO,
    RecordPaymentDTO,
    RecordActivityDTO,
    WeeklyCloseResultDTO,
    ParticipantSummaryDTO,
    GeneralSummaryDTO,
)


class ChallengeService:
    def __init__(self) -> None:
        self.participants: Dict[str, Participant] = {}
        self.weeks: Dict[int, ChallengeWeek] = {}
        self.pools: Dict[int, WeeklyPool] = {}
        self.accumulated_earnings: Dict[str, float] = {}
        self.participant_met_weeks: Dict[str, int] = {}
        self.participant_missed_weeks: Dict[str, int] = {}
        self.current_rollover: float = 0.0

    def register_participant(self, dto: RegisterParticipantDTO) -> Participant:
        """Registra un nuevo participante en el sistema."""
        if dto.id in self.participants:
            raise ValueError(f"Participante con ID {dto.id} ya existe")
        p = Participant(id=dto.id, name=dto.name)
        self.participants[dto.id] = p
        self.accumulated_earnings[dto.id] = 0.0
        self.participant_met_weeks[dto.id] = 0
        self.participant_missed_weeks[dto.id] = 0
        return p

    def record_payment(self, dto: RecordPaymentDTO) -> float:
        """Registra una aportacion economica para un participante."""
        if dto.participant_id not in self.participants:
            raise KeyError(f"Participante {dto.participant_id} no encontrado")
        participant = self.participants[dto.participant_id]
        participant.add_contribution(dto.amount)
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
        return activity.is_successful()

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
