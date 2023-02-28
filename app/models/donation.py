from sqlalchemy import Column, ForeignKey, Text, Integer

from app.core.db import Base
from .base import InvestBase


class Donation(Base, InvestBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    REPR_TEXT = (
        'Пожертвование пользователя ID {user_id}. '
        'Комментарий: {comment:15}. '
    )

    def __repr__(self):
        return self.REPR_TEXT.format(
            user_id=self.user_id,
            comment=self.comment
        ) + super().__repr__()
