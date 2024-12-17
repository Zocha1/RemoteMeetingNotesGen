# Dokumentacja API

## Endpoint `/add-meeting`

Ten endpoint służy do dodawania spotkań do bazy danych.

**Metoda:** `POST`

**Nagłówki:**
- `Content-Type: application/json`

**Body (JSON):**


- title (string): Tytuł spotkania.
- scheduled_time (string): Czas rozpoczęcia spotkania w formacie ISO 8601 (np. 2024-07-29T14:30:00).
- platform (string): Platforma, na której odbędzie się spotkanie.
Przykład:
```json
{
  "title": "Nazwa spotkania",
  "scheduled_time": "2024-07-29T14:30:00",
  "platform": "Zoom"
}
```
