Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:MidasMr/QRkot_spreadsheets.git
```

```
cd QRkot_spreadsheets
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

```
source venv/bin/activate
```

* Если у вас windows

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Работа с миграциями:

Выполнение всех неприменённых миграций
```
alembic upgrade head
```



Команда запуска проекта
```
uvicorn app.main:app --reload
```


Документация:

[Открыть документацию проекта](http://127.0.0.1:8000/docs)


Стек технологий:
```
Python 3.9
fastapi 0.78
sqlalchemy 1.4
alembic 1.7.7
aiogoogle 4.2
```


Автор:
[Александр Вязников(MidasMr)](https://github.com/MidasMr)