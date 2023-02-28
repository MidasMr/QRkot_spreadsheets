from datetime import datetime

from sqlalchemy import Boolean, Column, CheckConstraint, DateTime, Integer

from app.core.db import PreBase


class InvestBase(PreBase):
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('full_amount >= invested_amount')
    )

    REPR_TEXT_BASE = (
        'Полная сумма: {full_amount}, '
        'Инвестировання сумма: {invested_amount} '
        'Создано: {created}, Закрыто: {closed}'
    )

    def __repr__(self) -> str:
        return self.REPR_TEXT_BASE.format(
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            created=self.create_date,
            closed=self.close_date
        )
