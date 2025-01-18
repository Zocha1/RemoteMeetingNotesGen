# Remote Meeting Notes Generator

## Wymagania


## Instalacja

1.  **Klonowanie repozytorium:**
    ```bash
    git clone https://github.com/Zocha1/RemoteMeetingNotesGen.git
    ```

2.  **Dodanie rozszerzenia do przeglądarki (Chrome):**

    -  Otwórz przeglądarkę Chrome lub Edge.
    -  Wpisz w pasku adresu: `chrome://extensions`  i naciśnij Enter.
    -  Włącz tryb dewelopera (przełącznik w prawym górnym rogu).
    -  Kliknij przycisk "Załaduj rozpakowane".
    -  W oknie, które się pojawi, wskaż folder zawierający rozpakowane rozszerzenie ( folder `extension` z repozytorium).
    -  Rozszerzenie powinno się pojawić na liście.

2.  **Stworzenie i aktywacja środowiska wirtualnego:**
    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/macOS
    venv\Scripts\activate # Windows
    ```

3.  **Instalacja zależności (backend):**
    ```bash
    cd backend/
    pip install -r requirements.txt
    ```
# ... 

## Uruchomienie aplikacji

1. **Uruchomienie serwera flask:**
  ```bash
   cd backend/flask_api
   flask run
   ```
2. **Uruchomienie rozszerzenia:**
    - Po załadowaniu rozszerzenia jest ono gotowe do użytku.