from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation


def invest(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]],
) -> List[Union[CharityProject, Donation]]:
    changed_objects = []
    for source in sources:
        if target.invested_amount is None:
            target.invested_amount = 0
        donation_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for object in source, target:
            object.invested_amount += donation_amount
            if object.invested_amount == object.full_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        changed_objects.append(source)
        if target.fully_invested:
            break
    return changed_objects
