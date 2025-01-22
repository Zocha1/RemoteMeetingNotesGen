# Dokumentacja Frontendu: Remote Meeting Notes Generator

**Wersja:** 1.0

**Data:** 2024-22-01

## Architektura

Frontend składa się z kilku stron HTML, korzystających ze wspólnego szablonu `base.html`.  Strony te komunikują się z backendowym API za pomocą żądań **Fetch**.

## Strony

### `base.html`

**Opis:** Szablon bazowy dla wszystkich stron, zawiera nawigację i podstawową strukturę.

**Zawartość:**

- Pasek nawigacyjny z linkami do:
    - Home (`/home`)
    - Notes (`/notes`)
    - Plan Meeting (`/plan-meeting`)
- Blok `{% block content %}` do wstawiania zawartości specyficznej dla danej podstrony.
- Dołączony plik CSS: `base.css`

### `calendar.html`

**Opis:** Formularz planowania spotkań.

**Funkcjonalności:**

- Umożliwia wprowadzenie danych spotkania: tytułu, daty, czasu rozpoczęcia i zakończenia, oraz wybór platformy (Zoom, Google Meet, Microsoft Teams).
- Autoryzacja i synchronizacja z Google Calendar.
- Autoryzacja i synchronizacja z Zoom.
- Zapisanie danych spotkania w bazie danych (przez API `/add-meeting`).

**Elementy UI:**

- Formularz z polami tekstowymi, wyboru daty i czasu.
- Przyciski: "Authorize Google", "Sync with Google Calendar", "Authorize Zoom", "Sync with Zoom", "Save Meeting".

**Dołączone pliki:**

- CSS: `calendar.css`
- JS: `script.js`

### `home.html`

**Opis:** Strona główna aplikacji.

**Zawartość:**

- Powitalna wiadomość.
- Grafika ilustrująca funkcjonalność aplikacji.
- Opis kluczowych funkcji.

**Dołączone pliki:**

- CSS: `home.css`

### `notes.html`

**Opis:** Strona do zarządzania notatkami.

**Funkcjonalności:**

- Wyświetlanie listy spotkań.
- Przekierowanie do strony szczegółów spotkania po kliknięciu wiersza w tabeli.
- Menu kontekstowe z opcjami: "Export Note", "Summarize Note", "Find in Note", "Upload Screenshot".

**Elementy UI:**

- Tabela z listą spotkań.
- Menu kontekstowe.

**Dołączone pliki:**

- CSS: `notes.css`

### `meeting_details.html`

**Opis:**  Strona ze szczegółami spotkania.

**Zawartość:**

- Informacje o spotkaniu: ID, tytuł, czas, platforma.
- Transkrypcja i podsumowanie spotkania (jeśli dostępne).
- Przyciski: "Go back to notes", "Send Emails", "Download TXT", "Download Markdown", "Download HTML", "Download PDF".

**Dołączone pliki:**

- CSS: `meeting_details.css`

## JavaScript (`script.js`)

**Opis:** Plik JavaScript obsługujący interakcje użytkownika.

**Funkcje:**

- Przesyłanie formularza planowania spotkania (`/add-meeting`).
- Autoryzacja i synchronizacja z Google Calendar (`/authorize-google`, `/sync-google-calendar`).
- Autoryzacja i synchronizacja z Zoom (`/zoom/authorize`, `/zoom/sync-meeting`).
- Obsługa wyboru platformy w formularzu.
- Funkcje menu kontekstowego (aktualnie wyświetlają alerty).

## Style CSS

Każda strona HTML korzysta z dedykowanego pliku CSS, a dodatkowo dziedziczy style z `base.css`.
