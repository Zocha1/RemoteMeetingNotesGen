# Remote Meeting Notes Generator

## Instalacja aplikacji

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

3.  **Stworzenie i aktywacja środowiska wirtualnego:**
    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/macOS
    venv\Scripts\activate # Windows
    ```

4.  **Instalacja zależności (backend):**
    ```bash
    cd backend/
    pip install -r requirements.txt
    ```


5. **Dodanie pliku .env**

- W katalogu backend/flask_api utwórz plik **.env** z poniższą zawartością:

    ```bash
    ZOOM_CLIENT_ID=KLIENT_ID
    ZOOM_CLIENT_SECRET=SECRET
    ZOOM_REDIRECT_URI=http://localhost:5000/zoomoauthcallback

    COHERE_API_KEY=COHERE_API_KEY

    SENDINBLUE_API_KEY=SENDINBLUE_API_KEY
    SENDER_EMAIL=example@student.agh.edu.pl
    SENDER_NAME=NAME

    EMAILS_TO_SEND="example@gmail.com, example@student.agh.edu.pl"
    ```

- Aby aplikacja działała poprawnie, trzeba wygenerować wymagane klucze API:
  - Zoom: Utwórz aplikację w Zoom App Marketplace, aby uzyskać KLIENT_ID, SECRET oraz skonfigurować ZOOM_REDIRECT_URI.
  - Cohere: Zarejestruj się na Cohere i wygeneruj klucz API.
  - Sendinblue: Zarejestruj się na Sendinblue i wygeneruj klucz API.

## Instalacja dodatkowych narzędzi

### Instalacja FFmpeg

**Na systemach Windows:**
- Pobrać ze strony https://www.gyan.dev/ffmpeg/builds/ najnowszą wersję folderu “ffmpeg-git-essentials.7z” 
- Rozpakować pobrany folder
- Dodać ścieżkę do rozpakowanego folderu do zmiennej środowiskowej PATH

**Na systemach Linux:**
```
sudo apt install ffmpeg
```

### Instalacja Tesseract

#### **Na systemach Windows:**
1. Pobierz instalator dla Tesseract z oficjalnego repozytorium na GitHub:  
   [Tesseract OCR - GitHub Releases](https://github.com/tesseract-ocr/tesseract)
2. Zainstaluj Tesseract, postępując zgodnie z instrukcjami instalatora.
3. Po zakończeniu instalacji upewnij się, że ścieżka do katalogu instalacyjnego (np. `C:\Program Files\Tesseract-OCR`) została dodana do zmiennej środowiskowej **PATH**.

#### **Na systemach Linux:**
```bash
sudo apt install tesseract-ocr
```

## Uruchomienie aplikacji

1. **Uruchomienie serwera flask:**
  ```bash
   cd backend/flask_api
   flask run
   ```
2. **Uruchomienie rozszerzenia:**
    - Po załadowaniu rozszerzenia jest ono gotowe do użytku.
