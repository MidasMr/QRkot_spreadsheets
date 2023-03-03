from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


SPREADSHEET_TITLE = 'Отчет от {}'
ROWS = 100
COLUMNS = 3

SPREADSHEET_BODY = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROWS,
            columnCount=COLUMNS,
        )
    ))]
)

TABLE_HEAD = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

FORMAT = "%Y/%m/%d %H:%M:%S"

TABLE_VALUE_ERROR = (
    f'В таблице должно быть {ROWS} строк и {COLUMNS} столбцов. '
    'А было передано {rows_count} строк и {columns_count} столбцов'
)


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body: dict = SPREADSHEET_BODY
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = deepcopy(spreadsheet_body)
    spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
        now_date_time
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json={'type': 'user',
                  'role': 'writer',
                  'emailAddress': settings.email},
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = deepcopy(TABLE_HEAD)
    table_head[0][1] = now_date_time
    table_values = [
        *table_head,
        *[list(map(str, [
            project.name,
            project.close_date,
            project.description
        ])) for project in charity_projects]
    ]
    columns = max([len(row) for row in table_values])
    rows = len(table_values)
    if columns > COLUMNS or rows > ROWS:
        raise ValueError(TABLE_VALUE_ERROR.format(
            rows_count=rows,
            columns_count=columns
        ))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
