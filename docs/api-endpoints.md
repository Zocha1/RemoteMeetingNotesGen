
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

---

## Endpoint `/get-meetings`

Ten endpoint służy do pobierania danych o spotkaniach z bazy danych.

---

### **Metoda:**  
`GET`

---

### **Nagłówki:**  
- `Content-Type: application/json`

---

### **Odpowiedzi:**

**Sukces (200 OK):**
- W odpowiedzi na zapytanie, gdy istnieją spotkania w bazie danych, zwrócony zostanie obiekt JSON z listą spotkań.

```json
{
  "meetings": [
    {
      "meeting_id": 1,
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
  ],
  "message": "Meetings retrieved successfully"
}
```

**Błąd (500 Internal Server Error):**
- W przypadku błędu serwera:

```json
{
  "error": "Error while retrieving meetings: ..."
}
```

---

### **Uwagi:**
1. Jeśli baza danych jest pusta, odpowiedź zwróci pustą tablicę `meetings`:
   ```json
   {
     "meetings": [],
     "message": "Meetings retrieved successfully"
   }
   ```
2. W odpowiedzi mogą być zawarte wszystkie spotkania, w tym dane o spotkaniu, takie jak tytuł, czas, platforma i lista uczestników.

--- 


## Endpoint `/upload-audio`

Ten endpoint służy do przesyłania plików audio i ich transkrypcji do aktywnego spotkania.

---

### **Metoda:**

`POST`

---

### **Nagłówki:**

- `Content-Type: multipart/form-data`

---

### **Body (form-data):**

| Pole     | Typ   | Wymagane | Opis               |
|----------|-------|----------|--------------------|
| `file`   | file  | Tak      | Plik audio do przesłania. |

---

### **Przykład zapytania:**

```
(form-data)
file: <plik_audio.mp3>
```

---

### **Odpowiedzi:**

**Sukces (200 OK):**

```json
{
  "message": "Audio file saved successfully",
  "file_path": "/path/to/uploaded/audio/file"
}
```

**Błąd (400 Bad Request):**
- Jeśli brak pliku audio:
```json
{
  "error": "No audio file provided"
}
```
**Błąd (404 Not Found):**
- Gdy nie znaleziono żadnego spotkania w bazie danych:
```json
{
  "error": "No meeting found in database"
}
```
**Błąd (500 Internal Server Error):**
- W przypadku nieoczekiwanych błędów:
```json
{
    "error": "Failed to fetch last meeting ID: ..."
}
```
- W przypadku problemów z zapisem pliku:
```json
{
  "error": "Failed to save file: ..."
}
```
- W przypadku problemów z transkrypcją:
```json
{
  "error": "Failed to process audio: ..."
}
```

---

### **Uwagi:**

1. Plik audio jest zapisywany w folderze powiązanym z ID spotkania.
2. Transkrypcja pliku audio jest wykonywana po jego przesłaniu.
3. Wykorzystuje funkcję find_active_meeting aby zapisać plik audio do trwającego spotkania, w przypadku braku, zapisuje do ostatnio utworzonego.

---

## Endpoint `/upload-screenshot`

Ten endpoint służy do przesyłania screenów i ich przetworzenia (OCR) do aktywnego spotkania.

---

### **Metoda:**

`POST`

---

### **Nagłówki:**

-   `Content-Type: application/json`

---

### **Body (JSON):**

| Pole      | Typ    | Wymagane | Opis                 |
|-----------|--------|----------|----------------------|
| `image`  | string | Tak      | Dane obrazu w formacie base64 (z prefixem `"data:image/png;base64,"`). |

---

### **Przykład zapytania:**

```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

---

### **Odpowiedzi:**

**Sukces (200 OK):**

```json
{
  "message": "Screenshot and OCR processed successfully"
}
```

**Błąd (400 Bad Request):**

```json
{
  "error": "Image data is missing"
}
```
**Błąd (404 Not Found):**
 -  Gdy nie ma żadnego spotkania:

```json
{
  "error": "No meeting found in database"
}
```

**Błąd (500 Internal Server Error):**

```json
{
  "error": "..."
}
```

---

### **Uwagi:**

1.  Zdjęcie jest zapisywane w folderze powiązanym z ID spotkania.
2.  Jeśli zostanie wykryta tablica, zostaną utworzone i zapisane dodatkowe zdjęcia z przyciętymi fragmentami tablicy.
3.  Wykorzystuje funkcję find_active_meeting aby zapisać screen do trwającego spotkania, w przypadku braku, zapisuje do ostatnio utworzonego.

---

---

## Endpoint `/meeting-data`

Ten endpoint służy do pobierania danych o spotkaniach i ich transkrypcjach.

---

### **Metoda:**

`GET`

---

### **Nagłówki:**

- `Content-Type: application/json`

---

### **Odpowiedzi:**

**Sukces (200 OK):**

```json
[
  {
    "meeting_id": 1,
    "title": "Spotkanie zespołowe",
    "scheduled_time": "2024-07-29T14:30:00",
    "platform": "Zoom",
     "transcriptions": [
           {
            "transcription_id": 1,
            "full_text": "Transkrypcja spotkania...",
             "summary": "Podsumowanie spotkania..."
             }
            ]
  },
   {
     "meeting_id": 2,
    "title": "Spotkanie z klientem",
    "scheduled_time": "2024-07-29T16:30:00",
    "platform": "Google Meets",
     "transcriptions": []
  }
]
```

**Błąd (500 Internal Server Error):**

```json
{
  "error": "Failed to fetch data: ..."
}
```
---

### **Uwagi:**
1. Zwraca listę wszystkich spotkań w bazie danych, z dodatkowymi informacjami o transkrypcjach.
2. Transkrypcje są wyświetlane w postaci listy obiektów z `transcription_id`, `full_text` i `summary`.

---

## Endpoint `/meeting-details/<int:meeting_id>`

Ten endpoint służy do pobierania szczegółowych danych o konkretnym spotkaniu i jego transkrypcji oraz wyświetla je w szablonie HTML.

---

### **Metoda:**

`GET`

---

### **Nagłówki:**

- `Content-Type: application/json`

---

### **Parametry URL:**

| Parametr    | Typ      | Wymagane | Opis           |
|-------------|----------|----------|----------------|
| `meeting_id`| integer | Tak      | ID spotkania do pobrania. |

---

### **Odpowiedzi:**

**Sukces (200 OK):**
- Odpowiedź jest zwracana w postaci szablonu `meeting_details.html` z danymi o spotkaniu i transkrypcji.
**Błąd (404 Not Found):**
 -  W przypadku braku spotkania z danym ID:
```json
{
  "error": "Failed to fetch meeting data: ..."
}
```

---

### **Uwagi:**

1.  Endpoint renderuje szablon `meeting_details.html` z danymi spotkania i jego transkrypcją.
2.  Jeśli nie ma transkrypcji, transkrypt będzie ustawiony na None.

---


## Endpoint `/send-notes-email/<int:meeting_id>`

Ten endpoint służy do wysyłania notatek ze spotkania mailem.

---

### **Metoda:**

`POST`

---

### **Nagłówki:**

- `Content-Type: application/json`

---

### **Parametry URL:**

| Parametr    | Typ     | Wymagane | Opis                 |
|------------|---------|----------|----------------------|
| `meeting_id`| integer | Tak     | ID spotkania, którego notatki mają być wysłane. |

---

### **Odpowiedzi:**

**Sukces (200 OK):**

```json
{
  "message": "Email sent successfully"
}
```

**Błąd (404 Not Found):**

```json
{
  "error": "No transription found"
}
```

**Błąd (500 Internal Server Error):**

```json
{
  "error": "Failed to fetch meeting data: ..."
}
```

---

### **Uwagi:**

1.  Endpoint pobiera z bazy danych transkrypcję, podsumowanie i wyniki OCR dla danego spotkania.
2.  Wysyła wiadomość e-mail z notatkami na podany adres (zmien ten adres na właściwy do testów).
3. Wykorzystuje funkcję find_active_meeting aby wysłać notatki z trwającego spotkania, w przypadku braku, wysyła notatki z ostatnio utworzonego.
---
## Endpoint `/download-meeting-data/<string:output_format>/<int:meeting_id>`

Ten endpoint służy do pobierania danych spotkania w wybranym formacie (.txt, .md, .html lub .pdf).

---

### **Metoda:**
`GET`

---

### **Parametry URL:**
| Parametr        | Typ       | Wymagane | Opis                                                                        |
|-----------------|-----------|----------|-----------------------------------------------------------------------------|
| `output_format`| string    | Tak      | Format pliku do pobrania ('txt', 'md', 'html' lub 'pdf').                 |
| `meeting_id`   | integer  | Tak      | ID spotkania do pobrania.                                                  |

---

### **Odpowiedzi:**

**Sukces (200 OK):**
-  Zwraca plik z danymi spotkania w podanym formacie.

**Błąd (500 Internal Server Error):**

```json
{
  "error": "Failed to fetch data and generate {output_format} file: ..."
}
```

---
### **Uwagi:**
1. Parametr `output_format` określa format zwracanego pliku (txt, md, html, pdf)
2.  Endpoint wykorzystuje różne biblioteki do generowania różnych formatów plików (StringIO, WeasyPrint, ReportLab, pdfkit)
3.  Endpoint pobiera dane spotkania, transkrypcje oraz dane o OCR ze screenshotów

---
## Endpoint `/`
Ten endpoint to domyślny endpoint który kieruje nas do pliku `base.html`

---
### **Metoda:**
`GET`

---

### **Odpowiedzi:**
- Zwraca plik `base.html`
---
## Endpoint `/home`
Ten endpoint to domyślny endpoint który kieruje nas do pliku `home.html`

---
### **Metoda:**
`GET`

---

### **Odpowiedzi:**
- Zwraca plik `home.html`

---
## Endpoint `/recording`
Ten endpoint to domyślny endpoint który kieruje nas do pliku `recording.html`

---
### **Metoda:**
`GET`

---

### **Odpowiedzi:**
- Zwraca plik `recording.html`
---

## Endpoint `/notes`
Ten endpoint to domyślny endpoint który kieruje nas do pliku `notes.html`

---
### **Metoda:**
`GET`

---

### **Odpowiedzi:**
- Zwraca plik `notes.html`

---
## Endpoint `/plan-meeting`
Ten endpoint to domyślny endpoint który kieruje nas do pliku `calendar.html`

---
### **Metoda:**
`GET`

---

### **Odpowiedzi:**
- Zwraca plik `calendar.html`
---

## Endpoint `/authorize-google`
Ten endpoint służy do przekierowania użytkownika do serwisu Google aby autoryzował aplikację do korzystania z Google Calendar.

---
### **Metoda:**
`GET`

---

### **Odpowiedzi:**
-  Przekierowanie na adres autoryzacyjny Google

---
### **Uwagi:**
1. Ten endpoint nie zwraca żadnych danych JSON

---
## Endpoint `/oauth2callback`
Ten endpoint służy do odebrania tokenu autoryzacyjnego z Google Calendar.

---
### **Metoda:**
`GET`

---
### **Odpowiedzi:**
**Sukces (200 OK):**

```json
{
    "message": "Google Calendar connected successfully"
}
```
---
### **Uwagi:**
1. Ten endpoint odbiera dane z Google Calendar i zapisuje tokeny autoryzacyjne w sesji.
2. W sesji zapisywane są takie informacje jak token, refresh_token, token_uri, client_id, client_secret, scopes.

---
## Endpoint `/sync-google-calendar`
Ten endpoint służy do synchronizacji i utworzenia wydarzenia w kalendarzu google.

---
### **Metoda:**
`POST`

---

### **Nagłówki:**
- `Content-Type: application/json`

---
### **Body (JSON):**
| Pole | Typ | Wymagane | Opis |
|--------------|---------|-----------|-----------------------|
| `start_time` | string | Tak | Data i czas rozpoczęcia wydarzenia (format ISO 8601). |
| `end_time` | string | Tak | Data i czas zakończenia wydarzenia (format ISO 8601). |
| `title` | string | Nie | Tytuł wydarzenia. |
| `attendees` | array | Nie | Lista adresów email uczestników wydarzenia. |

---
### **Odpowiedzi:**

**Sukces (201 Created):**

```json
{
    "message": "Event created successfully",
    "event_id": "eventId"
}
```

**Błąd (400 Bad Request):**
```json
{
    "error": "Start time and end time are required"
}
```
```json
{
    "error": "End time must be after start time"
}
```
**Błąd (401 Unauthorized):**
```json
{
    "error": "Google Calendar not authorized"
}
```
**Błąd (500 Internal Server Error):**
```json
{
  "error": "..."
}
```

---
### **Uwagi:**
1. Wykorzystuje `credentials` z sesji
2. Domyślna strefa czasowa to UTC.

---

## Endpoint `/zoom/authorize`
Ten endpoint służy do przekierowania użytkownika do serwisu Zoom aby autoryzował aplikację do korzystania z API Zoom.

---
### **Metoda:**
`GET`

---
### **Odpowiedzi:**
-  Przekierowanie na adres autoryzacyjny Zoom

---
### **Uwagi:**
1. Ten endpoint nie zwraca żadnych danych JSON

---
## Endpoint `/zoom/oauth2callback`
Ten endpoint służy do odebrania tokenu autoryzacyjnego z Zoom API.

---
### **Metoda:**
`GET`

---
### **Parametry URL:**
| Parametr    | Typ     | Wymagane | Opis                 |
|------------|---------|----------|----------------------|
| `code` | string | Tak | Kod autoryzacyjny z Zoom. |

---

### **Odpowiedzi:**
**Sukces (200 OK):**
```json
{
    "message": "Zoom authorized successfully",
    "tokens": {
        "access_token": "...",
        "token_type": "bearer",
        "expires_in": 3600,
        "scope": "...",
        "refresh_token": "..."
    }
}
```

**Błąd (400 Bad Request):**
- Gdy kod autoryzacyjny nie jest dostępny
```json
{
    "error": "Authorization code not found"
}
```
**Błąd (Inne statusy):**
- Gdy autoryzacja nie powiodła się, zostanie zwrócony kod i odpowiedź JSON z Zoom API

```json
{
    "error": {
        "reason": "...",
        "message": "..."
    }
}
```
---
### **Uwagi:**
1. W sesji zapisywany jest jedynie `access_token`
2. Ten endpoint odbiera dane z Zoom API i zapisuje token autoryzacyjny w sesji.

---
## Endpoint `/zoom/create-meeting`
Ten endpoint służy do utworzenia nowego spotkania na platformie Zoom.

---
### **Metoda:**
`POST`

---

### **Nagłówki:**
- `Content-Type: application/json`

---
### **Body (JSON):**
- Body w formacie JSON jest wymagane, ale jego zawartość może nie być potrzebna do utworzenia spotkania w podstawowej wersji API Zoom.
---
### **Odpowiedzi:**
**Sukces (201 Created):**
 - W przypadku sukcesu zostanie zwrócony JSON z danymi spotkania z Zoom.
**Błąd (401 Unauthorized):**

```json
{
    "error": "User not authorized with Zoom"
}
```
**Błąd (Inne statusy):**
- Gdy autoryzacja nie powiodła się, zostanie zwrócony kod i odpowiedź JSON z Zoom API

```json
{
    "error": {
        "code": 124,
        "message": "Invalid access token"
    }
}
```
---
### **Uwagi:**
1. Wykorzystuje `access_token` z sesji.
2. Bazuje na domyślnych parametrach spotkania w API Zoom (przykładowy temat, typ, czas).
3. Wywołuje `https://api.zoom.us/v2/users/me/meetings`

---
## Endpoint `/zoom/sync-meeting`
Ten endpoint służy do utworzenia nowego spotkania na platformie Zoom i zapisania informacji w bazie danych lokalnie.

---
### **Metoda:**
`POST`

---

### **Nagłówki:**
- `Content-Type: application/json`

---
### **Body (JSON):**
| Pole        | Typ    | Wymagane | Opis                           |
|-------------|--------|----------|--------------------------------|
| `title`     | string | Nie      | Tytuł spotkania (opcjonalnie). |
| `start_time`| string | Tak      |  Czas rozpoczęcia spotkania (format ISO 8601). |
| `end_time`  | string | Tak      |  Czas zakończenia spotkania (format ISO 8601)     |
| `duration`  | integer | Nie     |  Czas trwania spotkania w minutach. |

---
### **Odpowiedzi:**
**Sukces (201 Created):**
```json
{
    "message": "Meeting synchronized with Zoom successfully",
    "zoom_meeting": {
        "id": 1234567890,
        "uuid": "...",
        "topic": "New Meeting",
        "join_url": "https://zoom.us/j/...",
    },
     "local_meeting_id": 1
}
```

**Błąd (400 Bad Request):**
- Jeśli brakuje wymaganych pól:
```json
{
    "error": "Start time and end time are required"
}
```

**Błąd (401 Unauthorized):**

```json
{
    "error": "User not authorized with Zoom"
}
```
**Błąd (Inne statusy):**
- Gdy autoryzacja nie powiodła się, zostanie zwrócony kod i odpowiedź JSON z Zoom API

```json
{
    "error": {
        "code": 124,
        "message": "Invalid access token"
    }
}
```
---
### **Uwagi:**
1. Wykorzystuje `access_token` z sesji.
2. Parametry spotkania jak title, start_time, end_time i duration są przekazywane w body jako JSON.
3. Zapisuje informacje o spotkaniu do bazy danych lokalnej.
4. Wywołuje `https://api.zoom.us/v2/users/me/meetings`
