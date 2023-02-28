from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class DonationCRUD(CRUDBase):

    async def get_dontion_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        d = donations.scalars().all()
        print(d)
        return d


donation_crud = DonationCRUD(Donation)
