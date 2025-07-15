# Review Sentiment API

Простой HTTP-сервис на FastAPI, который принимает отзывы, определяет их настроение (`positive`, `negative`, `neutral`) и сохраняет их в SQLite.

---

## Установка и запуск

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

---

## API эндпоинты

### 1. POST `/reviews`


```json
{
  "text": "Очень удобно, люблю ваш сервис"
}
```

- **Пример curl-запроса:**

```bash
curl -X POST http://127.0.0.1:8000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text": "Очень удобно, люблю ваш сервис"}'
```

- **Пример ответа:**

```json
{
  "id": 1,
  "text": "Очень удобно, люблю ваш сервис",
  "sentiment": "positive",
  "created_at": "2025-07-15T12:00:00.000000"
}
```

---

### 2. GET `/reviews?sentiment=...`

Возвращает список отзывов, отфильтрованных по настроению.


- **Query-параметры:**
  - `sentiment` (необязательный): `positive`, `negative`, `neutral`


- **Пример curl-запроса:**

```bash
curl "http://127.0.0.1:8000/reviews?sentiment=negative"
```

- **Пример ответа:**

```json
[
  {
    "id": 2,
    "text": "Глючит постоянно, неудобно пользоваться",
    "sentiment": "negative",
    "created_at": "2025-07-15T12:05:00.000000"
  },
  {
    "id": 3,
    "text": "Ненавижу, когда всё ломается",
    "sentiment": "negative",
    "created_at": "2025-07-15T12:07:00.000000"
  }
]
```

---

