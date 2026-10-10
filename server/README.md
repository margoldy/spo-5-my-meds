# Backend «Моя аптечка»

## Документация

- [Правила предметной области](../docs/domain-rules.md)
- [Структура баз данных и причины повторения полей](../docs/database-design.md)
- [Шифрование медицинских данных](../docs/encryption.md)
- [Описание API](docs/api.md)
- [Серверная схема базы данных](docs/server_bd.drawio.png)
- [Локальная схема базы данных](docs/local_bd.drawio.png)

## Запуск

1. Перейдите в папку сервера:

```powershell
cd server
```

2. Создайте и активируйте виртуальное окружение:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```


3. Установите зависимости:

```powershell
python -m pip install -r requirements.txt
```

4. Создайте PostgreSQL-базу с именем из `aptechka_db`.

5. Создайте файл `.env` на основе `.env.example` и укажите данные.

6. Создайте таблицы:

```powershell
python -m app.db.create_tables
```

7. Запустите сервер:

```powershell
python -m uvicorn app.main:app --reload
```

Сервер: <http://127.0.0.1:8000>

Swagger: <http://127.0.0.1:8000/docs>
