# Dokumentacja API

## Endpoint `/add-meeting`

Ten endpoint służy do dodawania spotkań oraz ich uczestników do bazy danych.

---

### **Metoda:**  
`POST`

---

### **Nagłówki:**  
- `Content-Type: application/json`

---

### **Body (JSON):**  

| Pole             | Typ       | Wymagane | Opis                                                        |
|------------------|-----------|----------|------------------------------------------------------------|
| `title`         | string    | Tak      | Tytuł spotkania.                                           |
| `scheduled_time`| string    | Tak      | Czas rozpoczęcia spotkania w formacie ISO 8601 (np. 2024-07-29T14:30:00). |
| `platform`      | string    | Tak      | Platforma, na której odbędzie się spotkanie (np. Zoom, Teams). |
| `participants`  | array     | Nie      | Lista uczestników spotkania (opcjonalnie).                 |
| `participants[].firstname` | string | Tak | Imię uczestnika.                                          |
| `participants[].lastname`  | string | Tak | Nazwisko uczestnika.                                      |
| `participants[].email`     | string | Tak | Adres e-mail uczestnika (musi być unikalny).              |

---

### **Przykład zapytania:**

```json
{
  "title": "Spotkanie zespołowe",
  "scheduled_time": "2024-07-29T14:30:00",
  "platform": "Zoom",
  "participants": [
    {
      "firstname": "Jan",
      "lastname": "Kowalski",
      "email": "jan.kowalski@example.com"
    },
    {
      "firstname": "Anna",
      "lastname": "Nowak",
      "email": "anna.nowak@example.com"
    }
  ]
}
```

---

### **Odpowiedzi:**

**Sukces (201 Created):**
```json
{
  "message": "Meeting and participants added successfully",
  "meeting_id": 1,
  "participants_added": 2
}
```

**Błąd (400 Bad Request):**
- Jeśli brakuje wymaganych pól:
```json
{
  "error": "Title, scheduled_time, and platform are required"
}
```

- Jeśli format daty jest nieprawidłowy:
```json
{
  "error": "Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS): ..."
}
```

- Jeśli uczestnik ma niekompletne dane:
```json
{
  "error": "Each participant must have firstname, lastname, and email"
}
```

**Błąd (500 Internal Server Error):**
- W przypadku nieoczekiwanych błędów:
```json
{
  "error": "Error while creating meeting: ..."
}
```

---

### **Uwagi:**
1. Jeżeli uczestnik o podanym adresie e-mail już istnieje w bazie, system automatycznie użyje istniejącego rekordu.
2. Każdy uczestnik musi mieć unikalny adres e-mail.
3. Jeżeli `participants` nie zostanie przesłane w zapytaniu, endpoint doda samo spotkanie bez uczestników.