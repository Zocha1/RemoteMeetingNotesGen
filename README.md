# Remote Meeting Notes Generator

## Opis projektu

Remote Meeting Notes Generator to aplikacja, która ma za zadanie automatycznie generować notatki ze spotkań online. Aplikacja jest podzielona na dwie główne części:

*   **Rozszerzenie przeglądarki:** Pozwala na interakcję ze stroną, na której odbywa się spotkanie, przechwytywanie transkrypcji, robienie screenshotów i akcje w czasie rzeczywistym.
*   **Backend (Flask API):** Odpowiada za obsługę danych z rozszerzenia, transkrypcję audio, rozpoznawanie tekstu ze zdjęć (OCR), generowanie podsumowań, wysyłanie notatek na e-mail oraz generowanie plików .txt, .md, .html i .pdf.

## Struktura projektu

Projekt składa się z następujących głównych folderów:

*   `backend/`: Zawiera kod backendu napisanego w Pythonie z wykorzystaniem frameworka Flask. Znajdują się tu również pliki konfiguracyjne.
*   `extension/`: Zawiera kod rozszerzenia przeglądarki, napisane w JavaScript.
*   `docs/`: Zawiera dokumentację projektu (patrz niżej).
*   `tests/`: Zawiera  testy backendu

## Dokumentacja

Cała dokumentacja projektu znajduje się w folderze `docs/`. W szczególności:

*   **Inżynieria Wymagań:** Opis wszystkich wymagań funkcjonalnych i niefunkcjonalnych projektu.
*   **Dokumentacja API:** Szczegółowy opis endpointów API backendu wraz z przykładami zapytań i odpowiedziami.
*   **Instrukcja Uruchomienia:** Krok po kroku instrukcja uruchomienia projektu na swoim komputerze, wraz z omówieniem zależności i konfiguracji środowiska.

## Instrukcja Uruchomienia

Pełna instrukcja uruchomienia projektu znajduje się w pliku [setup.md](https://github.com/Zocha1/RemoteMeetingNotesGen/blob/main/docs/setup.md) w folderze `docs` i opisuje:
   - instalację środowiska Python
   - instalację zależności
   - konfigurację zmiennych środowiskowych
   - konfigurację zewnętrznych API
   - start serwera backendowego
   - ładowanie rozszerzenia przeglądarki

## Technologie użyte

*   **Backend:** Python, Flask, SQLAlchemy, ReportLab, WeasyPrint, easyOCR, requests,  Pillow
*   **Rozszerzenie:** JavaScript, HTML, CSS
*   **Baza danych:**  SQLite
*   **API:** Google Calendar API, Zoom API, Cohere API, SENDINBLUE


