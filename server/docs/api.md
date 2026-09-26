
# Авторизация

## `POST /api/v1/auth/code/request`

Отправить одноразовый код на email.

**Доступ:** гость.

### Request

```json
{
  "email": "user@example.com"
}
```

### Response — `200 OK`

```json
{
  "message": "Код отправлен на email"
}
```

## `POST /api/v1/auth/code/verify`

Проверить код и войти. При первом входе пользователь создаётся автоматически.

**Доступ:** гость.

### Request

```json
{
  "email": "user@example.com",
  "code": "482913"
}
```

### Response — `200 OK`

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "6d8f3a10-91c7-4b1d-a4d8-9b102703f521",
    "email": "user@example.com",
    "role": "user",
    "created_at": "2026-09-18T10:00:00Z"
  }
}
```

## `POST /api/v1/auth/refresh`

Получить новую пару токенов.

**Доступ:** по `refresh_token`.

### Request

```json
{
  "refresh_token": "eyJ..."
}
```

### Response — `200 OK`

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

## `POST /api/v1/auth/logout`

Завершить текущую сессию.

**Доступ:** пользователь, администратор.

### Response — `204 No Content`

# Пользователь

## `GET /api/v1/users/me`

Получить профиль текущего пользователя.

**Доступ:** пользователь, администратор.

### Response — `200 OK`

```json
{
  "id": "6d8f3a10-91c7-4b1d-a4d8-9b102703f521",
  "name": "Дарья",
  "email": "user@example.com",
  "birth_date": "2006-04-15",
  "role": "user",
  "avatar_url": null,
  "created_at": "2026-09-18T10:00:00Z"
}
```

## `PATCH /api/v1/users/me`

Изменить профиль текущего пользователя. Email и роль через этот эндпоинт не изменяются.

**Доступ:** пользователь, администратор.

### Request

```json
{
  "name": "Дарья",
  "birth_date": "2006-04-15",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

### Response — `200 OK`

```json
{
  "id": "6d8f3a10-91c7-4b1d-a4d8-9b102703f521",
  "name": "Дарья",
  "email": "user@example.com",
  "birth_date": "2006-04-15",
  "role": "user",
  "avatar_url": "https://example.com/avatar.jpg",
  "created_at": "2026-09-18T10:00:00Z"
}
```

# Справочник лекарств

## `GET /api/v1/medications`

Получить активные лекарства из справочника.

**Доступ:** гость, пользователь, администратор.

### Query-параметры

`search`
`category`
`form`
`limit`
`offset`

### Response — `200 OK`

```json
{
  "items": [
    {
      "id": 4,
      "name": "Парацетамол",
      "international_name": "Paracetamol",
      "manufacturer": "Фармстандарт",
      "category": "antipyretic",
      "instruction_url": "https://example.com/instruction",
      "is_active": true,
      "form": "tablet",
      "strength": "500 мг"
    }
  ],
  "total": 1
}
```

## `GET /api/v1/medications/{medication_id}`

Получить лекарство из справочника по ID.

**Доступ:** гость, пользователь, администратор.

### Response — `200 OK`

```json
{
  "id": 4,
  "name": "Парацетамол",
  "international_name": "Paracetamol",
  "manufacturer": "Фармстандарт",
  "category": "antipyretic",
  "instruction_url": "https://example.com/instruction",
  "is_active": true,
  "form": "tablet",
  "strength": "500 мг"
}
```

## `POST /api/v1/medications`

Добавить лекарство в справочник.

**Доступ:** администратор.

### Request

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

### Response — `201 Created`

```json
{
  "id": 4,
  "name": "Парацетамол",
  "international_name": "Paracetamol",
  "manufacturer": "Фармстандарт",
  "category": "antipyretic",
  "instruction_url": "https://example.com/instruction",
  "is_active": true,
  "form": "tablet",
  "strength": "500 мг"
}
```

## `PATCH /api/v1/medications/{medication_id}`

Изменить лекарство или убрать его из каталога через `is_active: false`.

**Доступ:** администратор.

### Request


```json
{
  "manufacturer": "Новый производитель",
  "instruction_url": "https://example.com/new-instruction",
  "is_active": false
}
```

### Response — `200 OK`

```json
{
  "id": 4,
  "name": "Парацетамол",
  "international_name": "Paracetamol",
  "manufacturer": "Новый производитель",
  "category": "antipyretic",
  "instruction_url": "https://example.com/new-instruction",
  "is_active": false,
  "form": "tablet",
  "strength": "500 мг"
}
```

# Курсы лекарств

## `GET /api/v1/courses`

Получить курсы текущего пользователя.

**Доступ:** аутентифицированный пользователь; возвращаются только собственные курсы.

### Response — `200 OK`

```json
{
  "items": [
    {
      "id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
      "medication_id": 4,
      "custom_name": null,
      "display_name": "Витрум",
      "start_date": "2026-09-18",
      "end_date": "2026-09-23",
      "is_active": true,
      "taking_mode": "scheduled",
      "schedules": [
        {
          "scheduled_at": "15:00",
          "dose_amount": 1,
          "dose_unit": "tablet",
          "days_of_week": [1, 2, 3, 4, 5, 6, 7]
        }
      ],
      "notes": "После еды",
      "created_at": "2026-09-18T10:00:00Z"
    }
  ]
}
```

## `POST /api/v1/courses`

Создать курс лекарства.

**Доступ:** аутентифицированный пользователь; курс создаётся для текущего пользователя.

### Request — лекарство из справочника

```json
{
  "medication_id": 4,
  "start_date": "2026-09-18",
  "end_date": "2026-09-23",
  "notes": "После еды"
}
```

### Request — пользовательское лекарство

```json
{
  "custom_name": "Моё лекарство",
  "start_date": "2026-09-18",
  "end_date": null,
  "notes": null
}
```

Нужно передать ровно одно из полей: `medication_id` или `custom_name`. Курс без расписаний допустим: для него `taking_mode` возвращается как `as_needed`.

### Response — `201 Created`

```json
{
  "id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "medication_id": 4,
  "custom_name": null,
  "start_date": "2026-09-18",
  "end_date": "2026-09-23",
  "is_active": true,
  "notes": "После еды",
  "created_at": "2026-09-18T10:00:00Z"
}
```

## `GET /api/v1/courses/{course_id}`

Получить курс по ID.

**Доступ:** владелец курса. Роль администратора не даёт доступ к чужим медицинским данным.

### Response — `200 OK`

```json
{
  "id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "medication_id": 4,
  "custom_name": null,
  "start_date": "2026-09-18",
  "end_date": "2026-09-23",
  "is_active": true,
  "taking_mode": "scheduled",
  "notes": "После еды",
  "created_at": "2026-09-18T10:00:00Z",
  "medication": {
    "id": 4,
    "name": "Парацетамол",
    "form": "tablet",
    "strength": "500 мг"
  },
  "schedules": [
    {
      "id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
      "scheduled_at": "09:00",
      "dose_amount": 1,
      "dose_unit": "tablet",
      "days_of_week": [1, 2, 3, 4, 5, 6, 7]
    }
  ]
}
```

## `PATCH /api/v1/courses/{course_id}`

Изменить курс.

**Доступ:** владелец курса. Роль администратора не даёт доступ к чужим медицинским данным.

### Request

Передаются только изменяемые поля.

```json
{
  "end_date": "2026-09-30",
  "is_active": false,
  "notes": "Курс завершён"
}
```

### Response — `200 OK`

```json
{
  "id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "medication_id": 4,
  "custom_name": null,
  "start_date": "2026-09-18",
  "end_date": "2026-09-30",
  "is_active": false,
  "notes": "Курс завершён",
  "created_at": "2026-09-18T10:00:00Z"
}
```

## `DELETE /api/v1/courses/{course_id}`

Удалить курс.

**Доступ:** владелец курса. Роль администратора не даёт доступ к чужим медицинским данным.

### Response — `204 No Content`

# Расписание

`days_of_week` использует значения от `1` (понедельник) до `7` (воскресенье). Один курс может не иметь ни одной записи расписания — это режим «по необходимости».

В объекте `Schedule` поле `scheduled_at` содержит время суток в формате `HH:MM`. В готовой карточке конкретного дня это же поле содержит уже вычисленные дату, время и часовой пояс.

## `GET /api/v1/courses/{course_id}/schedules`

Получить расписание курса.

**Доступ:** владелец курса. Роль администратора не даёт доступ к чужим медицинским данным.

### Response — `200 OK`

```json
{
  "items": [
    {
      "id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
      "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
      "scheduled_at": "09:00",
      "dose_amount": 1,
      "dose_unit": "tablet",
      "days_of_week": [1, 2, 3, 4, 5, 6, 7]
    }
  ]
}
```

## `POST /api/v1/courses/{course_id}/schedules`

Добавить время и дозу приёма. Для разных доз создаются отдельные записи расписания.

**Доступ:** владелец курса. Роль администратора не даёт доступ к чужим медицинским данным.

### Request

```json
{
  "scheduled_at": "09:00",
  "dose_amount": 1,
  "dose_unit": "tablet",
  "days_of_week": [1, 2, 3, 4, 5, 6, 7]
}
```


### Response — `201 Created`

```json
{
  "id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "scheduled_at": "09:00",
  "dose_amount": 1,
  "dose_unit": "tablet",
  "days_of_week": [1, 2, 3, 4, 5, 6, 7]
}
```

## `GET /api/v1/schedules`

Получить готовые карточки приёмов для экрана календаря на указанную дату. Сервер разворачивает повторяющееся расписание, объединяет его с фактическими приёмами и возвращает статус; клиент не вычисляет дни недели сам.

**Доступ:** аутентифицированный пользователь; возвращается только собственное расписание.

**Параметры запроса:**

- `date` — обязательный параметр в формате `YYYY-MM-DD`.

### Request

```http
GET /api/v1/schedules?date=2026-09-18
```

### Response — `200 OK`

```json
{
  "date": "2026-09-18",
  "items": [
    {
      "schedule_id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
      "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
      "scheduled_at": "2026-09-18T09:00:00+03:00",
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

`status` принимает значения `pending` или `taken`.

## `PATCH /api/v1/schedules/{schedule_id}`

Изменить время, дозу или дни недели.

**Доступ:** владелец курса. Роль администратора не даёт доступ к чужим медицинским данным.

### Request

Передаются только изменяемые поля.

```json
{
  "scheduled_at": "10:00",
  "dose_amount": 0.5,
  "days_of_week": [1, 3, 5]
}
```

### Response — `200 OK`

```json
{
  "id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "scheduled_at": "10:00",
  "dose_amount": 0.5,
  "dose_unit": "tablet",
  "days_of_week": [1, 3, 5]
}
```

## `DELETE /api/v1/schedules/{schedule_id}`

Удалить запись расписания.

**Доступ:** владелец курса. Роль администратора не даёт доступ к чужим медицинским данным.

### Response — `204 No Content`

# Приёмы лекарств

`user_id` сервер получает из access-токена и не принимает от клиента. Для запланированного приёма обязательны `course_id` и `schedule_id`. Внеплановый приём можно связать с курсом либо сохранить с `course_id: null` и `schedule_id: null`.

Каждый `Intake` хранит фактические `dose_amount`, `dose_unit` и `medication_name`. Это снимок на момент приёма: последующее изменение расписания, курса или справочника не меняет историю.

Для планового приёма клиент подставляет дозу из расписания, но пользователь может изменить фактически принятую дозу перед подтверждением. Название сервер получает из курса. Для отдельной записи без курса клиент передаёт только текстовое `medication_name`; `medication_id` в `Intake` не сохраняется и курс автоматически не создаётся.

## `POST /api/v1/intakes`

Записать фактический приём лекарства.

**Доступ:** аутентифицированный пользователь. Если указан курс, он должен принадлежать текущему пользователю; отдельная запись принадлежит пользователю из access-токена.

### Request — запланированный приём

```json
{
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "schedule_id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
  "taken_at": "2026-09-18T09:07:00+03:00",
  "dose_amount": 1,
  "dose_unit": "tablet"
}
```

### Request — внеплановый приём

```json
{
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "schedule_id": null,
  "taken_at": "2026-09-18T15:30:00+03:00",
  "dose_amount": 0.5,
  "dose_unit": "tablet"
}
```

### Request — отдельный приём без курса

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

Если лекарство выбрано из справочника, клиент передаёт его отображаемое название в `medication_name`. Идентификатор `medication_id` в исторической записи не сохраняется.

### Response — `201 Created`

```json
{
  "id": "bb67f43b-923a-4f70-a56d-8b93796695dc",
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "schedule_id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
  "taken_at": "2026-09-18T09:07:00+03:00",
  "dose_amount": 1,
  "dose_unit": "tablet",
  "medication_name": "Эсциталопрам"
}
```

## `GET /api/v1/intakes`

Получить историю приёмов текущего пользователя.

**Доступ:** аутентифицированный пользователь; возвращается только собственная история приёмов.

### Query-параметры

| Параметр | Тип | Описание |
| --- | --- | --- |
| `course_id` | `UUID` | Фильтр по курсу |
| `from` | `datetime` | Начало периода |
| `to` | `datetime` | Конец периода |

### Response — `200 OK`

```json
{
  "items": [
    {
      "id": "bb67f43b-923a-4f70-a56d-8b93796695dc",
      "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
      "schedule_id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
      "taken_at": "2026-09-18T09:07:00+03:00",
      "dose_amount": 1,
      "dose_unit": "tablet",
      "medication_name": "Эсциталопрам"
    }
  ]
}
```

## `PATCH /api/v1/intakes/{intake_id}`

Исправить фактическое время или дозу приёма. Название-снимок через этот эндпоинт не изменяется.

**Доступ:** владелец записи. Роль администратора не даёт доступ к чужим медицинским данным.

### Request

Передаются только изменяемые поля.

```json
{
  "taken_at": "2026-09-18T09:15:00+03:00",
  "dose_amount": 0.5,
  "dose_unit": "tablet"
}
```

### Response — `200 OK`

```json
{
  "id": "bb67f43b-923a-4f70-a56d-8b93796695dc",
  "course_id": "4c29955a-20e2-4f20-a8dd-22a0fb581f75",
  "schedule_id": "7e96c55d-e1af-46fc-a1e5-f1b8ddf0472b",
  "taken_at": "2026-09-18T09:15:00+03:00",
  "dose_amount": 0.5,
  "dose_unit": "tablet",
  "medication_name": "Эсциталопрам"
}
```

## `DELETE /api/v1/intakes/{intake_id}`

Удалить ошибочную запись о приёме.

**Доступ:** владелец записи. Роль администратора не даёт доступ к чужим медицинским данным.

### Response — `204 No Content`
