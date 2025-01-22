# Dokumentacja inżynierii wymagań

## Członkowie zespołu

- [Zofia ](https://github.com/Zocha1)
- [Marta ](https://github.com/marpom03)
- [Paweł ](https://github.com/pawel-rus)

## 1. Macierz kompetencji zespołu

| Kompetencje                                             | Zofia | Marta | Paweł |
|---------------------------------------------------------|-------|-------|-------|
| Bazy Danych SQL                                         | ✅    | ✅    | ✅   |
| Bazy Danych NoSQL                                       | ❌    | ❌    | ✅   |
| Znajomość technologii AI/ML                             | ✅    | ✅    | ❌   |
| Znajomość narzędzi OCR                                  | ✅    | ✅    | ❌   |
| Znajomość PyTorch / TensorFlow                          | ✅    | ✅    | ❌   |
| Znajomość platformy Hugging Face                        | ✅    | ❌    | ❌   |
| Znajomość WebRTC                                        | ❌    | ❌    | ❌   |
| Tworzenie wtyczek do przeglądarek (Chrome, Firefox)     | ❌    | ❌    | ✅   |
| Znajomość Flask / Django                                | ❌    | ❌    | ✅   |
| Znajomość Node.js, Express.js                           | ❌    | ✅    | ❌   |
| Znajomość Java Spring                                   | ❌    | ❌    | ❌   |
| Frontend Frameworks (Vue.js, Angular, React)            | ✅    | ✅    | ❌   |
| Znajomość TypeScript                                    | ✅    | ✅    | ❌   |
| DevOps / CI/CD (GitHub Actions)                         | ❌    | ❌    | ✅   |
| Praca z chmurą (AWS, GCP, Azure)                        | ❌    | ❌    | ✅   |
| Konteneryzacja - Docker                                 | ❌    | ❌    | ✅   |
| Testowanie (unit, integracyjne)                         | ❌    | ❌    | ❌   |
| Postman (testowanie API)                                | ❌    | ❌    | ✅   |
| Praca z API do transkrypcji mowy (np. Google Cloud, AWS)| ❌    | ❌    | ❌   |
| Praca z narzędziami analitycznymi (ElasticSearch, Kibana)| ❌   | ❌    | ❌   |
| Integracja z modelami generatywnymi (ChatGPT, Gemini AI, Cloud AI) | ❌ | ❌ | ✅ |
| Integracja z kalendarzami (Google, Outlook)             | ❌    | ❌   | ❌    |
| Project Management                                      | ✅    | ❌   | ❌    |


## 2. Zestaw pytań dotyczących wymagań

| Pytanie                                          | Odpowiedź                                                                              | Uwagi                                             |
|--------------------------------------------------|----------------------------------------------------------------------------------------|---------------------------------------------------|
| Jaka ma to być aplikacja? Webowa czy Desktopowa? | Webowa lub plugin do przeglądarki.                                                     | Powinna działać niezależnie od narzędzia do telekonferencji. |
| Ilu użytkowników będzie korzystać z aplikacji?   | Nieokreślona liczba, zakładamy wsparcie dla dowolnej liczby uczestników w spotkaniach. | Skalowalność.                                     |
| Jakie dane mają być przetwarzane?                | Transkrypcja mowy, zrzuty ekranu, treści OCR.                    | -                                                 |
| Jakie formaty eksportu są wymagane?              | PDF, HTML, TXT, MD.                                                                    | -                                                 |
| Jakie platformy do spotkań mają być wspierane?   | Zoom, Microsoft Teams, Google Meet.                                                    | Możliwość rozbudowy o inne platformy.             |
| Czy aplikacja powinna działać automatycznie?     | Powinna zapisywać utworzone spotkania do kalendarza w danej aplikacji, np Google Calendar.                 | Integracja z kalendarzem.                         |
| Czy raporty mają być wysyłane automatycznie?     | Tak, e-mailem do uczestników spotkania.                                                | Brevo (ex Sendinblue), Margin                       |
| Czy aplikacja ma identyfikować mówców?           | Tak, to opcjonalna funkcjonalność.                                      | Może wymagać zaawansowanego przetwarzania danych. |
| Czy potrzebne są dodatkowe analizy statystyczne? | Tak, opcjonalnie analiza ilości i szybkości wypowiedzi uczestników.                    | So omówienia z klientem.           |



## 3. Funkcjonalności

| Funkcjonalność                      | Opis                                                                      | Uwagi                          |
|-------------------------------------|---------------------------------------------------------------------------|--------------------------------|
| Transkrypcja tekstu mówionego       | Automatyczna zamiana mowy na tekst.                                       | -                              |
| Zapis zrzutu ekranu                 | Możliwość zapisu prezentacji udostępnianej przez dowolnego użytkownika.   | -                              |
| OCR - Optical Character Recognition | Rozpoznawanie tekstu w obrazach, np. z whiteboarda.                       | -                              |
| Generowanie notatki ze spotkania    | Eksport notatek w formatach: PDF, HTML, TXT, MD.                          | -                              |
| Raport po spotkaniu                 | Automatyczne wysyłanie raportu e-mailem do uczestników.                   | Brevo (ex Sendinblue), Margin  |
| Integracja z kalendarzem            | Automatyczne dodawanie zaplanowanych spotkań.                             | W google Calendar, zaplanowanie spotkania na Zoom |
| Wsparcie dla platform               | Obsługa Zoom, Microsoft Teams, Google Meet.                               | -                              |
| Identyfikacja mówców                | Przypisywanie wypowiedzi do konkretnych osób.                             | Opcjonalnie - "nice to have".  |
| Podsumowanie notatek                | Wyciąganie kluczowych informacji.                                         | -                              |
| Wyszukiwanie w notatkach            | Szybkie znajdowanie konkretnych treści.                                   | -                              |
| Statystyki wypowiedzi               | Analiza ilości i szybkości wypowiedzi uczestników.                        | Opcjonalnie - "nice to have".  |



## 4. Ustalony format danych wejściowych

### Struktura bazy danych:

---

### Tabela: `users`
Przechowuje informacje o użytkownikach aplikacji.

| Kolumna       | Typ danych      | Opis                                              |
|---------------|-----------------|---------------------------------------------------|
| `user_id`     | `INT`           | Unikalny identyfikator uczestnika  (klucz główny) |
| `firstname`   | `VARCHAR(50)`   | Imię  uczestnika                                  |
| `lastname`    | `VARCHAR(50)`   | Nazwisko  uczestnika                              |
| `email`       | `VARCHAR(120)`  | Adres e-mail uczestnika                           |

#### Przykład danych wejściowych:
| user_id | firstname | lastname | email                |
|---------|-----------|----------|----------------------|
| 1       | Zofia     |  M       | zofia@example.com    |
| 2       | Marta     |  P       | marta@example.com    |
| 3       | Paweł     |  R       | pawel@example.com    |

---

### Tabela: `meetings`
Przechowuje dane dotyczące spotkań.

| Kolumna         | Typ danych      | Opis                                              |
|------------------|-----------------|---------------------------------------------------|
| `meeting_id`     | `INT`           | Unikalny identyfikator spotkania (klucz główny)   |
| `title`          | `VARCHAR(255)`  | Tytuł spotkania                                   |
| `scheduled_time` | `DATETIME`      | Data i godzina zaplanowanego spotkania           |
| `platform`       | `VARCHAR(50)`   | Platforma używana podczas spotkania (np. Zoom)   |

#### Przykład danych wejściowych:
| meeting_id | title               | scheduled_time      | platform        | 
|------------|---------------------|---------------------|-----------------|
| 1          | Planowanie projektu | 2024-02-01 09:00:00 | Zoom            | 
| 2          | Warsztat OCR        | 2024-02-02 10:00:00 | Microsoft Teams |
| 3          | Analiza AI          | 2024-02-03 11:00:00 | Google Meet     |

---

### Tabela: `participants`
Przechowuje relacje między użytkownikami a spotkaniami.

| Kolumna           | Typ danych      | Opis                                             |
|-------------------|-----------------|--------------------------------------------------|
| `participant_id`  | `INT`           | Unikalny identyfikator uczestnictwa (klucz główny)|
| `meeting_id`      | `INT`           | ID spotkania, w którym użytkownik uczestniczy    |
| `user_id`         | `INT`           | ID użytkownika uczestniczącego w spotkaniu       |
| `role`            | `VARCHAR(50)`   | Rola użytkownika w spotkaniu (`Host`, `Guest`)   |

#### Przykład danych wejściowych:
| participant_id | meeting_id | user_id | role         |
|----------------|------------|---------|--------------|
| 1              | 1          | 1       | Host         |
| 2              | 1          | 2       | Guest        | 
| 3              | 2          | 2       | Host         |
| 4              | 3          | 3       | Guest        |

---

### Tabela: `transcriptions`
Przechowuje pełne dane transkrypcji ze spotkań.

| Kolumna             | Typ danych      | Opis                                              |
|---------------------|-----------------|---------------------------------------------------|
| `transcription_id`  | `INT`           | Unikalny identyfikator transkrypcji (klucz główny)|
| `meeting_id`        | `INT`           | ID spotkania, którego dotyczy transkrypcja        |
| `full_text`         | `TEXT`          | Pełna treść transkrypcji                          |
| `summary`           | `TEXT`          | Podsumowanie transkrypcji                         |
| `created_at`        | `DATETIME`      | Data i godzina wygenerowania transkrypcji         |

#### Przykład danych wejściowych:
| transcription_id | meeting_id | full_text                                          | summary          | created_at          |
|------------------|------------|----------------------------------------------------|------------------|---------------------|
| 1                | 1          | "Witamy na spotkaniu. Omówimy harmonogram..."      | Na spotkaniu ... | 2024-02-01 12:00:00 |
| 2                | 2          | "Zapraszam na warsztaty OCR. Rozpoczynamy od..."   | Podsumowanie     | 2024-02-02 14:00:00 |
| 3                | 3          | "Analiza modeli AI. Przedstawiamy wyniki testów..."| Podsumowanie     | 2024-02-03 15:00:00 |

---


### Tabela: `screenshots`
Przechowuje zapisane obrazy ekranów ze spotkań.

| Kolumna          | Typ danych      | Opis                                               |
|------------------|-----------------|----------------------------------------------------|
| `screenshot_id`  | `INT`           | Unikalny identyfikator zrzutu ekranu (klucz główny)|
| `meeting_id`     | `INT`           | ID spotkania, w którym wykonano zrzut ekranu       |
| `image_path`     | `VARCHAR(255)`  | Ścieżka do pliku ze zrzutem ekranu                 |
| `timestamp`      | `DATETIME`      | Czas wykonania zrzutu ekranu                       |

#### Przykład danych wejściowych:
| screenshot_id | meeting_id | image_path            | timestamp           |
|---------------|------------|-----------------------|---------------------|
| 1             | 1          | /screenshots/1_01.png | 2024-02-01 09:30:00 |
| 2             | 2          | /screenshots/2_01.png | 2024-02-02 10:45:00 |
| 3             | 3          | /screenshots/3_01.png | 2024-02-03 11:20:00 |

---

### Tabela: `ocr`
Przechowuje wyniki analizy OCR.

| Kolumna          | Typ danych      | Opis                                              |
|------------------|-----------------|---------------------------------------------------|
| `ocr_id`         | `INT`           | Unikalny identyfikator wyniku OCR (klucz główny)  |
| `screenshot_id`  | `INT`           | ID zrzutu ekranu, którego dotyczy analiza OCR     |
| `text`           | `TEXT`          | Rozpoznany tekst                                  |
| `confidence`     | `FLOAT`         | Poziom pewności rozpoznania tekstu (0-100)        |

#### Przykład danych wejściowych:
| ocr_id | screenshot_id | text                          | confidence |
|--------|---------------|-------------------------------|------------|
| 1      | 1             | "Plan projektu"               | 98.5       |
| 2      | 2             | "Warsztaty"                   | 95.2       |
| 3      | 3             | "Analiza modeli AI"           | 96.7       |
 


## 5. Modelowanie systemu za pomocą tabeli i przepływ danych

| **Aktorzy**      | Użytkownik końcowy, serwer aplikacji, analityk danych      |
|------------------|----------------------------------------------------------|
| **Opis**         | Celem działania systemu jest przetwarzanie i analizowanie danych zdalnych spotkań, takich jak transkrypcje mowy, zrzuty ekranu oraz OCR. System generuje raporty oraz podsumowania, które są automatycznie wysyłane do uczestników. |
| **Dane**         | Pliki dźwiękowe, obrazy (zrzuty ekranu, zdjęcia tablic), treść transkrypcji, dane uczestników spotkania, informacje z kalendarza. |
| **Wyzwalacz**    | Manualne uruchomienie nagrywania ekranu przez użytkownika za pomocą wtyczki. |
| **Odpowiedź**    | Raport z danymi spotkania, transkrypcją, podsumowaniem, tekstem ze zrzutów ekranu wykrytym OCR. |
| **Uwagi**        | - Wysoka dokładność OCR oraz transkrypcji. <br> - Możliwość przetwarzania danych dla wielu platform telekonferencyjnych (Zoom, Teams, Google Meet). |



## 6. Diagram przypadków użycia

```mermaid
graph LR
    A[Start Spotkania] --> B[Transkrypcja tekstu mówionego]
    A --> C[Generowanie zrzutów ekranu]
    C --> D[Zapis zrzutów ekranu]
    D --> E[OCR - Rozpoznawanie tekstu]
    B --> I[Dodaj tekst do transkrypcji]
    I --> J[Generowanie notatek]
    E --> J
    J --> K[Generowanie pliku PDF, TXT, HTML lub MD]
    K --> L[Wysłanie e-mail do wszystkich uczestników]

    AA[Planowanie spotkania] --> AB[Integracja z kalendarzem] --> AC[Integracja z Zoom, MS Teams, Google Meet]

```

## 7. Diagram sekwencyjny UML: 

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



### 8. Sugerowany Stack technologiczny :

<div style="display: flex; align-items: center; gap: 10px;">
    <a href="https://www.python.org/" target="_blank" rel="noreferrer">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="85" height="85"/>
    </a>
    <a href="https://www.postgresql.org/" target="_blank" rel="noreferrer">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" alt="PostgreSQL" width="85" height="85"/>
    </a>
    <a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/flask/flask-original.svg" alt="Flask" width="85" height="85"/>
    </a>
     <a href="https://sqlite.org/index.html" target="_blank" rel="noreferrer">
         <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg" alt="SQLite" width="85" height="85"/>
     </a> 
    <a href="https://developer.mozilla.org/en-US/docs/Web/HTML" target="_blank" rel="noreferrer"> 
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" alt="HTML" width="85" height="85"/> 
    </a> 
    <a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank" rel="noreferrer"> 
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" alt="CSS" width="85" height="85"/> 
    </a> 
    <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> 
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="JavaScript" width="85" height="85"/> 
    </a>
</div>

#### Uzasadnienie wyboru technologii

#### **Python**  
Python został wybrany ze względu na bogaty ekosystem bibliotek wspierających kluczowe funkcjonalności projektu. Model Whisper od Open-AI umożliwi transkrypcję mowy,  Tesseract OCR do rozpoznawania tekstu z obrazów. Python doskonale nadaje się do przetwarzania języka naturalnego (NLP) oraz integracji z systemami zewnętrznymi.

#### **Flask**  
Flask to lekki framework webowy, który umożliwia elastyczną budowę backendu. Jego prostota pozwala na szybkie tworzenie API, zarządzanie sesjami użytkowników oraz obsługę zapytań HTTP.

#### **SQLite**
SQLite to lekka baza danych, która świetnie sprawdza się w projektach o mniejszej skali i uproszczonej architekturze. Dzięki brakowi potrzeby uruchamiania osobnego serwera, SQLite oferuje szybkie wdrożenie i prostą konfigurację. Jest doskonałym wyborem do przechowywania danych takich jak transkrypcje, zrzuty ekranu czy wyniki OCR w lokalnych aplikacjach lub środowiskach testowych.

#### **HTML, CSS, JavaScript**
Technologie frontendowe HTML, CSS i JavaScript zostaną wykorzystane do stworzenia interfejsu użytkownika w postaci wtyczki jak i stron do zarządzania spotkaniami i notatkami.

- **HTML** pozwala na budowę struktury stron i formularzy używanych przez użytkowników.
  
- **CSS** przyda się w dostosowaniu stylistyki aplikacji
  
- **JavaScript** umożliwi dynamiczne reakcje na działania użytkownika oraz integrację wtyczki z backendem.
