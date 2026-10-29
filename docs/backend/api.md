# API

Базовый путь: `/api/v1`.

Медицинские данные телефон шифрует до отправки. Сервер принимает `encrypted_data` как готовую непрозрачную строку и не может её расшифровать. Все медицинские запросы работают только с данными пользователя из access-токена.

### `GET /health/`

Проверяет, что API запущен. Возвращает `{ "status": "ok" }`.

## Авторизация

### `POST /auth/code/request`

```json
{ "email": "user@example.com" }
```

Отправляет шестизначный код. Новый код можно запросить через минуту. Код действует 5 минут, допускается не более 5 неверных попыток.

### `POST /auth/code/verify`

```json
{ "email": "user@example.com", "code": "671234" }
```

Создаёт пользователя при первом входе и возвращает `access_token`, `refresh_token` и `user`. Access-токен действует 30 минут, refresh-токен — 30 дней.

### `POST /auth/token/refresh`

```json
{ "refresh_token": "eyJ..." }
```

Возвращает новый `access_token`.

## Профиль и ключ шифрования

### `GET /users/me`

Возвращает `id`, `name`, `email`, `birth_date`, `role`, `avatar_url`, `timezone` и `created_at`.

### `PATCH /users/me`

Изменяет переданные `name`, `birth_date`, `avatar_url` и `timezone`.

### `GET /users/me/encryption-key`

Возвращает сохранённый `encrypted_dek`. Если ключ ещё не создан, возвращает `404`.

### `PUT /users/me/encryption-key`

```json
{ "encrypted_dek": "строка, созданная телефоном" }
```

Создаёт или заменяет зашифрованный `DEK`. В строку телефон сам упаковывает salt Argon2id, nonce AES-GCM, ciphertext и tag. Пароль и открытый `DEK` на сервер не передаются.

## Справочник лекарств

### `GET /medications`

Параметры: `search`, `category`, `form`, `limit`, `offset`. Гость и пользователь видят активные записи, администратор — все.

### `GET /medications/{medication_id}`

Возвращает одно лекарство.

### `POST /medications`

Только для администратора.

```json
{
  "name": "Парацетамол",
  "international_name": "Paracetamol",
  "manufacturer": "Фармстандарт",
  "category": "antipyretic",
  "instruction_url": "https://example.com/instruction",
  "form": "tablet",
  "strength": "500 мг"
}
```

### `PATCH /medications/{medication_id}`

Только для администратора. `is_active: false` скрывает запись без удаления.

## Курсы

Содержимое курса шифруется одним `encrypted_data`. Внутри телефон хранит выбранное лекарство или своё название и заметки. Открытыми остаются даты и состояние курса.

### `GET /courses`

Возвращает курсы текущего пользователя с расписаниями.

### `POST /courses`

```json
{
  "start_date": "2026-09-18",
  "end_date": null,
  "encrypted_data": "зашифрованные данные курса"
}
```

Курс без расписаний имеет `taking_mode: "as_needed"`.

### `GET /courses/{course_id}`

Возвращает собственный курс.

### `PATCH /courses/{course_id}`

Изменяет `start_date`, `end_date`, `is_active` и `encrypted_data`.

### `DELETE /courses/{course_id}`

Удаляет курс и его расписания. История приёмов сохраняется.

## Расписание

Время и дни недели остаются открытыми, чтобы сервер мог построить календарь. Доза и единица измерения находятся внутри `encrypted_data`.

### `GET /courses/{course_id}/schedules`

Возвращает расписания курса.

### `POST /courses/{course_id}/schedules`

```json
{
  "scheduled_at": "09:00",
  "days_of_week": [1, 2, 3, 4, 5, 6, 7],
  "encrypted_data": "зашифрованная доза"
}
```

### `PATCH /schedules/{schedule_id}`

Изменяет `scheduled_at`, `days_of_week` и `encrypted_data`.

### `DELETE /schedules/{schedule_id}`

Удаляет расписание, но не историю.

### `GET /schedules?date=YYYY-MM-DD`

Возвращает карточки календаря в часовом поясе пользователя. Каждый элемент содержит `planned_at`, `status`, `course_data`, `schedule_data` и найденный приём.

## Приёмы

`user_id` берётся из access-токена. Название лекарства и фактическая доза хранятся внутри `encrypted_data` как снимок на момент приёма.

### `POST /intakes`

```json
{
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "schedule_id": null,
  "taken_at": "2026-09-18T18:40:00+03:00",
  "encrypted_data": "зашифрованный снимок приёма"
}
```

Для отдельной записи без курса оба идентификатора передаются как `null`.

### `GET /intakes`

Параметры: `course_id`, `from`, `to`. `from` и `to` передаются со смещением часового пояса.

### `PATCH /intakes/{intake_id}`

Изменяет `taken_at` и `encrypted_data`.

### `DELETE /intakes/{intake_id}`

Удаляет ошибочную запись владельца.
