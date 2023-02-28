from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_charity_project_before_removing,
    check_charity_project_before_edit
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)
from app.services.invest import invest


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project, session, commit=False
    )
    uninvested_donations = await donation_crud.get_uninvested(
        session
    )
    session.add_all(invest(charity_project, uninvested_donations))
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.get(
    '/closed',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_closed_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_projects_by_completion_rate(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_before_edit(
        project_id, obj_in, session
    )
    if obj_in.full_amount is not None and (
        obj_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=422,
            detail='нельзя установить требуемую сумму меньше уже вложенной!'
        )
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_before_removing(
        project_id, session
    )
    return await charity_project_crud.remove(charity_project, session)
