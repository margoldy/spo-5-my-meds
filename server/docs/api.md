# API

Базовый путь: `/api/v1`. Все медицинские запросы работают только с данными пользователя из access-токена. Роль администратора приложения не даёт доступ к чужим курсам и истории.

Фактические моменты времени передаются в ISO 8601 со смещением, например `2026-09-18T09:07:00+03:00`. Подробные ограничения собраны в [правилах предметной области](../../docs/domain-rules.md).

## Авторизация

### `POST /auth/code/request`

Отправляет одноразовый код. Доступен гостю.

```json
{ "email": "user@example.com" }
```

Ответ `200 OK`: `{ "message": "Код отправлен на email" }`.

### `POST /auth/code/verify`

Проверяет код и создаёт пользователя при первом входе.

```json
{ "email": "user@example.com", "code": "482913" }
```

Ответ `200 OK`:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "6d8f3a10-91c7-4b1d-a4d8-9b102703f521",
    "email": "user@example.com",
    "role": "user"
  }
}
```

## Профиль

### `GET /users/me`

Возвращает профиль текущего пользователя:

```json
{
  "id": "6d8f3a10-91c7-4b1d-a4d8-9b102703f521",
  "name": "Макан",
  "email": "user@example.com",
  "birth_date": "2006-04-15",
  "role": "user",
  "avatar_url": null,
  "created_at": "2026-09-18T10:00:00Z"
}
```

### `PATCH /users/me`

Изменяет `name`, `birth_date` и `avatar_url`. Email и роль здесь не изменяются. Возвращает обновлённый профиль.

## Справочник лекарств

Объект лекарства содержит: `id`, `name`, `international_name`, `manufacturer`, `category`, `instruction_url`, `form`, `strength`, `is_active`.

### `GET /medications`

Возвращает `{ "items": [...], "total": 0 }`.

Параметры: `search`, `category`, `form`, `limit`, `offset`. Гость и пользователь видят только активные записи; администратор может видеть скрытые.

### `GET /medications/{medication_id}`

Возвращает одну запись справочника.

### `POST /medications`

Добавляет препарат. Доступен только администратору.

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

Ответ `201 Created` содержит созданный объект.

### `PATCH /medications/{medication_id}`

Изменяет переданные поля. `is_active: false` скрывает препарат без удаления. Доступен только администратору.

## Курсы

### `GET /courses`

Возвращает `{ "items": [...] }` с курсами текущего пользователя. Курс включает `display_name`, вычисляемый `taking_mode` и массив `schedules`.

### `POST /courses`

Создаёт курс. Нужно передать ровно одно из полей: `medication_id` или `custom_name`.

Из справочника:

```json
{
  "medication_id": 4,
  "start_date": "2026-09-18",
  "end_date": "2026-09-23",
  "notes": "После еды"
}
```

С собственным названием:

```json
{
  "custom_name": "Моё лекарство",
  "start_date": "2026-09-18",
  "end_date": null,
  "notes": null
}
```

Ответ `201 Created` содержит созданный курс. Отсутствие расписаний означает режим `as_needed`.

### `GET /courses/{course_id}`

Возвращает собственный курс вместе с лекарством и расписаниями.

### `PATCH /courses/{course_id}`

Изменяет переданные поля курса: `start_date`, `end_date`, `is_active`, `notes`. Возвращает обновлённый курс.

### `DELETE /courses/{course_id}`

Удаляет собственный курс. Его расписания удаляются, а история приёмов сохраняется. Ответ `204 No Content`.

## Расписание

`days_of_week` содержит уникальные числа от `1` (понедельник) до `7` (воскресенье). `scheduled_at` в объекте расписания — время суток в формате `HH:MM`.

### `GET /courses/{course_id}/schedules`

Возвращает `{ "items": [...] }` с расписаниями курса.

### `POST /courses/{course_id}/schedules`

Добавляет одно время и дозу в собственный курс.

```json
{
  "scheduled_at": "09:00",
  "dose_amount": 1,
  "dose_unit": "tablet",
  "days_of_week": [1, 2, 3, 4, 5, 6, 7]
}
```

Ответ `201 Created` содержит созданное расписание.

### `PATCH /schedules/{schedule_id}`

Изменяет переданные поля `scheduled_at`, `dose_amount`, `dose_unit` и `days_of_week`. Возвращает обновлённое расписание.

### `DELETE /schedules/{schedule_id}`

Удаляет расписание, не удаляя историю. Ответ `204 No Content`.

### `GET /schedules?date=YYYY-MM-DD`

Возвращает карточки календаря на один локальный день. Сервер разворачивает повторяющиеся расписания и сопоставляет их с фактическими приёмами.

```json
{
  "date": "2026-09-18",
  "items": [
    {
      "schedule_id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
      "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
      "planned_at": "2026-09-18T09:00:00+03:00",
      "display_name": "Эсциталопрам",
      "dose_amount": 1,
      "dose_unit": "tablet",
      "status": "taken",
      "intake": {
        "id": "bb67f43b-923a-4f70-a56d-8b93796695dc",
        "taken_at": "2026-09-18T09:03:00+03:00"
      }
    }
  ]
}
```

`status` равен `pending` или `taken`.

## Приёмы

`user_id` берётся из access-токена и клиентом не передаётся. Каждый `Intake` хранит снимок `medication_name`, `dose_amount` и `dose_unit`.

### `POST /intakes`

Плановый приём:

```json
{
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "schedule_id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
  "taken_at": "2026-09-18T09:07:00+03:00",
  "dose_amount": 1,
  "dose_unit": "tablet"
}
```

Приём из существующего курса вне расписания отличается только `schedule_id: null`.

Отдельная запись без курса:

```json
{
  "course_id": null,
  "schedule_id": null,
  "taken_at": "2026-09-18T18:40:00+03:00",
  "dose_amount": 5,
  "dose_unit": "мл",
  "medication_name": "Сироп от кашля"
}
```

Для отдельной записи передаётся только название, даже если оно выбрано из справочника. `medication_id` не сохраняется, курс не создаётся. Ответ `201 Created` содержит созданный `Intake`.

### `GET /intakes`

Возвращает `{ "items": [...] }` с историей текущего пользователя.

Параметры: `course_id`, `from`, `to`. Записи с `course_id = null` также входят в общую историю.

### `PATCH /intakes/{intake_id}`

Исправляет переданные `taken_at`, `dose_amount` и `dose_unit`. Название-снимок не изменяется. Возвращает обновлённый `Intake`.

### `DELETE /intakes/{intake_id}`

Удаляет ошибочную запись владельца. Ответ `204 No Content`.
