from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectUpdate
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_project_id_by_name(
        room_name, session
    )
    if room_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_before_edit(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
):
    print(obj_in)
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    full_amount = obj_in.full_amount
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    elif obj_in.description is None and full_amount is None:
        raise HTTPException(
            status_code=422,
            detail='Нельзя назначать пустое имя, описание или цель фонда'
        )
    if full_amount is None:
        full_amount = 0
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='нельзя установить требуемую сумму меньше уже вложенной!'
        )
    return charity_project


async def check_charity_project_before_removing(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail=(
                'В проект были внесены средства, не подлежит удалению!'
            )
        )
    return charity_project
