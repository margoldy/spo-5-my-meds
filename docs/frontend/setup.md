# Настройка и запуск frontend

1. Перейдите в папку frontend:

```powershell
cd frontend
```

2. Установите зависимости:

```powershell
npm install
```

3. Создайте `.env` на основе [`.env.example`](../../frontend/.env.example):

```powershell
Copy-Item .env.example .env
```

Для локального запуска оставьте адрес backend:

```env
VITE_API_URL=http://127.0.0.1:8000
```

4. Запустите frontend:

```powershell
npm run dev
```

Приложение будет доступно по адресу <http://127.0.0.1:5173>.

Для опубликованного frontend укажите в `VITE_API_URL` публичный HTTPS-адрес backend и соберите проект заново.

## Проверка сборки

```powershell
npm run build
```
