# Backend «Моя аптечка»

## Запуск

1. Перейдите в папку сервера:

```powershell
cd server
```

2. Создайте и активируйте виртуальное окружение:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Установите зависимости:

```powershell
pip install -r requirements.txt
```

4. Создайте PostgreSQL-базу `moya_aptechka` и выполните в ней скрипт `create_database.sql`.

5. Создайте файл `.env` на основе `.env.example` и укажите настройки PostgreSQL, JWT и почты.

6. Запустите сервер:

```powershell
uvicorn app.main:app --reload
```

Сервер: <http://127.0.0.1:8000>

Swagger: <http://127.0.0.1:8000/docs>
