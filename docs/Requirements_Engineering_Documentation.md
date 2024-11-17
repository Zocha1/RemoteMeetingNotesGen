# Dokumentacja inżynierii wymagań

## Członkowie zespołu

- [Zofia](https://github.com/Zocha1)
- [Marta](https://github.com/marpom03)
- [Paweł](https://github.com/pawel-rus)

## 1. Macierz kompetencji zespołu

| Kompetencje                     | Zofia | Marta | Paweł |
|---------------------------------|--------|-------|-------|
| Bazy Danych SQL                | ❌     | ❌    | ❌    |
| Bazy Danych NoSQL              | ❌     | ❌    | ❌    |
| Znajomość technologii AI/ML    | ✅     | ✅    | ❌    |
| Praca z API do transkrypcji mowy (np. Google, AWS) | ❌ | ❌    | ❌    |
| Znajomość narzędzi OCR         | ✅     | ✅    | ❌    |
| React TS                       | ❌     | ❌    | ❌    |
| Znajomość Flask / Django       | ❌     | ❌    | ❌    |
| Znajomość Node.js, Express.js  | ❌     | ❌    | ❌    |
| Znajomość Java                 | ❌     | ❌    | ❌    |
| Zarządzanie plikami i formatami dokumentów (PDF, HTML) | ❌ | ❌    | ❌    |
| Frontend Frameworks (Vue.js, Angular) | ❌     | ❌    | ❌    |
| DevOps / CI/CD (np. Jenkins, GitHub Actions) | ❌ | ❌    | ❌    |
| Praca z chmurą (AWS, GCP, Azure) | ❌    | ❌    | ❌    |
| Docker                         | ❌     | ❌    | ❌    |
| Testowanie                     | ❌     | ❌    | ❌    |
| Postman                        | ❌     | ❌    | ❌    |
| Praca z narzędziami analitycznymi (ElasticSearch, Kibana) | ❌ | ❌ | ❌ |
| Znajomość WebRTC               | ❌     | ❌    | ❌    |
| Project Management             | ❌     | ❌    | ❌    |


## 2. Zestaw pytań dotyczących wymagań

| Pytanie                                         | Odpowiedź                                                                                     | Uwagi                          |
|------------------------------------------------|---------------------------------------------------------------------------------------------|--------------------------------|
| Jaka ma to być aplikacja? Webowa czy Desktopowa? | Webowa lub plugin do przeglądarki.                                                           | Powinna działać niezależnie od narzędzia do telekonferencji. |
| Czy aplikacja wymaga logowania?                 | Nie wspomniano, ale jest to raczej oczywiste.                        | Warto omówić na spotkaniu.    |
| Ilu użytkowników będzie korzystać z aplikacji? | Nieokreślona liczba, zakładamy wsparcie dla dowolnej liczby uczestników w spotkaniach.         | Skalowalność.                 |
| Jakie dane mają być przetwarzane?              | Transkrypcja mowy, zrzuty ekranu, treści OCR, identyfikacja mówców.                          | -                              |
| Jakie formaty eksportu są wymagane?            | PDF, HTML, TXT, MD.                                                                          | -                              |
| Jakie platformy do spotkań mają być wspierane? | Zoom, Microsoft Teams, Google Meet.                                                         | Możliwość rozbudowy o inne platformy. |
| Czy aplikacja powinna działać automatycznie?   | Tak, z automatycznym uruchamianiem na podstawie wydarzeń w kalendarzu.                       | Integracja z kalendarzem.     |
| Czy raporty mają być wysyłane automatycznie?   | Tak, e-mailem do uczestników spotkania.                                                     | Do omówienia dokładny system mailowy. |
| Czy aplikacja ma identyfikować mówców?         | Tak, to opcjonalna funkcjonalność (nice to have).                                            | Może wymagać zaawansowanego przetwarzania danych. |
| Czy potrzebne są dodatkowe analizy statystyczne? | Tak, opcjonalnie analiza ilości i szybkości wypowiedzi uczestników.                          | Do omówienia z klientem.      |


## 3. Funkcjonalności

| Funkcjonalność                        | Opis                                                                                      | Uwagi                          |
|--------------------------------------|------------------------------------------------------------------------------------------|--------------------------------|
| Transkrypcja tekstu mówionego        | Automatyczna zamiana mowy na tekst.                                                      | -                              |
| Zapis zrzutu ekranu                  | Możliwość zapisu prezentacji udostępnianej przez dowolnego użytkownika.                  | -                              |
| OCR - Optical Character Recognition  | Rozpoznawanie tekstu w obrazach, np. z whiteboarda.                                      | -                              |
| Generowanie notatki ze spotkania     | Eksport notatek w formatach: PDF, HTML, TXT, MD.                                         | -                              |
| Raport po spotkaniu                  | Automatyczne wysyłanie raportu e-mailem do uczestników.                                  | SEND IN BLUE(Brevo), MARGUN   |
| Integracja z kalendarzem             | Automatyczne uruchamianie nagrywania na podstawie zaplanowanych wydarzeń.                | -                              |
| Wsparcie dla platform                | Obsługa Zoom, Microsoft Teams, Google Meet.                                              | -                              |
| Identyfikacja mówców                 | Przypisywanie wypowiedzi do konkretnych osób.                                            | Opcjonalnie - "nice to have". |
| Podsumowanie notatek                 | Wyciąganie kluczowych informacji.                                                        | -                              |
| Wyszukiwanie w notatkach             | Szybkie znajdowanie konkretnych treści.                                                  | -                              |
| Statystyki wypowiedzi                | Analiza ilości i szybkości wypowiedzi uczestników.                                       | Opcjonalnie - "nice to have". |


## 4. Ustalony format danych wejściowych

### Struktura bazy danych:

### Tabela: `users`:

| Kolumna       | Typ danych     | Opis                                              |
| ------------- | -------------- | ------------------------------------------------- |
| `id`          | `INT`          | Unikalny identyfikator użytkownika (klucz główny) |
| `username`    | `VARCHAR(50)`  | Nazwa użytkownika                                 |
| `password`    | `VARCHAR(255)` | Hash hasła                                        |
| `email`       | `VARCHAR(100)` | Firmowy email użytkownika                         |
| `role`        | `VARCHAR(10)`  | Rola użytkownika (`admin` albo `user`)            |

#### Przykład danych wejściowych:

| id  | username   | password                           | email                | role  |
| --- | ---------- | ---------------------------------- | -------------------- | ----- |
| 1   | admin      | $2y$10$abcdefghijkmnopqrstuvwxyz   | admin@example.com    | admin |
| 2   | jsmith     | $2y$10$lmnopqrstuvwxyzabcdefghijk  | jsmith@example.com   | user  |
| 3   | amiller    | $2y$10$zxywvutsrqponmlkjihgfedcba  | amiller@example.com  | user  |

---

### Tabela: `meetings`

| Kolumna        | Typ danych     | Opis                                                   |
| -------------- | -------------- | ------------------------------------------------------ |
| `id`           | `INT`          | Unikalny identyfikator spotkania (klucz główny)         |
| `title`        | `VARCHAR(100)` | Tytuł spotkania                                        |
| `description`  | `TEXT`         | Opis spotkania                                         |
| `start_time`   | `DATETIME`     | Data i godzina rozpoczęcia spotkania                   |
| `end_time`     | `DATETIME`     | Data i godzina zakończenia spotkania                   |
| `created_by`   | `INT`          | ID użytkownika, który utworzył spotkanie (klucz obcy) |

#### Przykład danych wejściowych:

| id  | title                 | description           | start_time           | end_time             | created_by |
| --- | --------------------- | --------------------- | -------------------- | -------------------- | ---------- |
| 1   | Spotkanie projektowe   | Omówienie postępu projektu | 2024-11-20 09:00:00 | 2024-11-20 10:00:00 | 1          |
| 2   | Spotkanie zarządu      | Dyskusja na temat strategii | 2024-11-21 11:00:00 | 2024-11-21 12:30:00 | 2          |
| 3   | Spotkanie z klientem   | Prezentacja wyników  | 2024-11-22 14:00:00 | 2024-11-22 15:00:00 | 3          |

---

### Tabela: `transcriptions`

| Kolumna          | Typ danych     | Opis                                                   |
| ---------------- | -------------- | ------------------------------------------------------ |
| `id`             | `INT`          | Unikalny identyfikator transkrypcji (klucz główny)      |
| `meeting_id`     | `INT`          | ID spotkania (klucz obcy)                              |
| `speaker_id`     | `INT`          | ID mówcy (klucz obcy do tabeli `users`)                |
| `text`           | `TEXT`         | Zapis transkrypcji tekstu                              |
| `timestamp`      | `DATETIME`     | Czas, w którym wypowiedź została zarejestrowana        |

#### Przykład danych wejściowych:

| id  | meeting_id | speaker_id | text                            | timestamp           |
| --- | ---------- | ---------- | ------------------------------- | ------------------- |
| 1   | 1          | 1          | "Witam wszystkich na spotkaniu." | 2024-11-20 09:01:00 |
| 2   | 1          | 2          | "Omówię postępy w projekcie."    | 2024-11-20 09:03:15 |
| 3   | 2          | 3          | "Chciałbym przedstawić nasze cele." | 2024-11-21 11:05:00 |

---

### Tabela: `screenshots`

| Kolumna          | Typ danych     | Opis                                                   |
| ---------------- | -------------- | ------------------------------------------------------ |
| `id`             | `INT`          | Unikalny identyfikator zrzutu ekranu (klucz główny)     |
| `meeting_id`     | `INT`          | ID spotkania (klucz obcy)                              |
| `image_url`      | `VARCHAR(255)` | URL do obrazu zrzutu ekranu                             |
| `timestamp`      | `DATETIME`     | Czas zrobienia zrzutu ekranu                            |

#### Przykład danych wejściowych:

| id  | meeting_id | image_url                            | timestamp           |
| --- | ---------- | ------------------------------------ | ------------------- |
| 1   | 1          | "https://example.com/screenshot1.png" | 2024-11-20 09:10:00 |
| 2   | 2          | "https://example.com/screenshot2.png" | 2024-11-21 11:10:00 |
| 3   | 3          | "https://example.com/screenshot3.png" | 2024-11-22 14:20:00 |

---

### Tabela: `reports`

| Kolumna         | Typ danych     | Opis                                                   |
| --------------- | -------------- | ------------------------------------------------------ |
| `id`            | `INT`          | Unikalny identyfikator raportu (klucz główny)           |
| `meeting_id`    | `INT`          | ID spotkania (klucz obcy)                              |
| `file_type`     | `VARCHAR(10)`  | Typ pliku (np. PDF, TXT, HTML, MD)                     |
| `file_url`      | `VARCHAR(255)` | URL do wygenerowanego raportu                           |
| `created_at`    | `DATETIME`     | Czas utworzenia raportu                                |

#### Przykład danych wejściowych:

| id  | meeting_id | file_type | file_url                             | created_at          |
| --- | ---------- | --------- | ------------------------------------ | ------------------- |
| 1   | 1          | PDF       | "https://example.com/report1.pdf"    | 2024-11-20 10:05:00 |
| 2   | 2          | HTML      | "https://example.com/report2.html"   | 2024-11-21 12:35:00 |
| 3   | 3          | MD        | "https://example.com/report3.md"     | 2024-11-22 15:05:00 |

---

### Tabela: `calendar_integration`

| Kolumna         | Typ danych     | Opis                                                   |
| --------------- | -------------- | ------------------------------------------------------ |
| `id`            | `INT`          | Unikalny identyfikator wpisu (klucz główny)             |
| `meeting_id`    | `INT`          | ID spotkania (klucz obcy)                              |
| `calendar_event`| `VARCHAR(255)` | Identyfikator wydarzenia w kalendarzu (np. Google Calendar) |
| `status`        | `VARCHAR(20)`  | Status integracji (np. 'Zakończono', 'W trakcie')      |

#### Przykład danych wejściowych:

| id  | meeting_id | calendar_event           | status   |
| --- | ---------- | ------------------------ | -------- |
| 1   | 1          | "event_id_12345"         | Zakończono |
| 2   | 2          | "event_id_67890"         | W trakcie |
| 3   | 3          | "event_id_54321"         | Zakończono |


## 5. Diagram przypadków użycia

```mermaid
graph LR
    A[Start Spotkania] --> B[Transkrypcja tekstu mówionego]
    A --> C[Generowanie zrzutów ekranu]
    C --> D[Zapis zrzutów ekranu]
    D --> E[OCR - Rozpoznawanie tekstu]
    B --> F{Identyfikacja mówcy}
    F -- Użytkownik A --> G[Przypisz wypowiedź A]
    F -- Użytkownik B --> H[Przypisz wypowiedź B]
    G --> I[Dodaj tekst do transkrypcji]
    H --> I
    I --> J[Generowanie notatek]
    E --> J
    J --> K[Generowanie pliku PDF, TXT, HTML lub MD]
    K --> L[Wysłanie e-mail do wszystkich uczestników]

    AA[Integracja z kalendarzem] --> AB[Automatyczne uruchamianie nagrywania]
    AB --> AC[Integracja z Zoom, MS Teams, Google Meet]

```

## 6. Diagram sekwencyjny UML: 

```mermaid
sequenceDiagram
    participant USER
    participant FRONTEND
    participant BACKEND
    participant DATABASE

    USER->>FRONTEND: 1. Start Spotkania
    FRONTEND->>BACKEND: 2. Rozpocznij transkrypcję mówionego tekstu
    BACKEND->>DATABASE: 3. Zapisz transkrypcję
    DATABASE-->>BACKEND: 4. Potwierdzenie zapisu transkrypcji
    BACKEND-->>FRONTEND: 5. Przesyłanie transkrypcji do frontendu

    USER->>FRONTEND: 6. Generowanie zrzutów ekranu
    FRONTEND->>BACKEND: 7. Zapis zrzutów ekranu
    BACKEND->>DATABASE: 8. Zapisz zrzut ekranu
    DATABASE-->>BACKEND: 9. Potwierdzenie zapisu zrzutów
    BACKEND-->>FRONTEND: 10. Zapisano zrzuty ekranu

    BACKEND->>BACKEND: 11. Rozpoznawanie tekstu z OCR
    BACKEND->>DATABASE: 12. Zapisanie tekstu z OCR
    DATABASE-->>BACKEND: 13. Potwierdzenie zapisu OCR

    FRONTEND->>BACKEND: 14. Generowanie notatki ze spotkania
    BACKEND->>DATABASE: 15. Zapisanie notatki
    DATABASE-->>BACKEND: 16. Potwierdzenie zapisu notatki
    BACKEND-->>FRONTEND: 17. Wygenerowanie pliku (PDF, TXT, HTML)

    BACKEND->>USER: 18. Wysłanie e-maila z notatką do uczestników
    BACKEND-->>USER: 19. Potwierdzenie wysyłki e-maila

```



### 7. Sugerowany Stack technologiczny :

<div style="display: flex; align-items: center; gap: 10px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" alt="React" width="140" height="140">
    <img src="https://upload.wikimedia.org/wikipedia/commons/d/d9/Node.js_logo.svg" alt="Node.js" width="140" height="140"> 
    <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" alt="PostgreSQL" width="140" height="140"> 
</div>

#### Uzasadnienie wyboru technologii

**React**
- Jest doskonałym narzędziem do budowania interaktywnych interfejsów użytkownika, co pozwala na płynne doświadczenia dla użytkowników aplikacji webowej. 

**Node.js**
- Działa na architekturze zdarzeniowej, co pozwala na obsługę wielu jednoczesnych połączeń, idealne do aplikacji wymagających dużej wydajności.
- Użycie JavaScript zarówno po stronie klienta, jak i serwera upraszcza procesy rozwoju i umożliwia zespołowi większą elastyczność w pracy. Programiści mogą łatwiej przechodzić między front-endem a back-endem.

**PostgreSQL**
- To potężna relacyjna baza danych, która obsługuje dużą ilość danych, zapewniając wysoką wydajność i wsparcie dla zaawansowanych funkcji.