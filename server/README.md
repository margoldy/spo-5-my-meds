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

> В PowerShell используйте именно `py -3.13`, а не Python из Git Bash/MSYS2:
> он создаёт Windows-окружение с папкой `Scripts`.

3. Установите зависимости:

```powershell
python -m pip install -r requirements.txt
```

4. Создайте PostgreSQL-базу с именем из `DB_NAME`. При первом запуске приложение создаст таблицы через SQLAlchemy.

5. Создайте файл `.env` на основе `.env.example` и укажите настройки PostgreSQL, JWT и почты.

6. Запустите сервер:

```powershell
python -m uvicorn app.main:app --reload
```

Сервер: <http://127.0.0.1:8000>

Swagger: <http://127.0.0.1:8000/docs>
