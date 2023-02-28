from sqlalchemy import Column, String, Text

from app.core.db import Base
from .base import InvestBase


class CharityProject(Base, InvestBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    REPR_TEXT = 'Проект {name:15}. Описание: {description:15}. '

    def __repr__(self):
        return self.REPR_TEXT.format(
            name=self.name,
            description=self.description
        ) + super().__repr__()
