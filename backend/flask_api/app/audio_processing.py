import speech_recognition as sr
from pydub import AudioSegment
import os
from datetime import datetime
from flask import jsonify
import whisper
import cohere
from .models import db, Transcriptions, Meetings


def _convert_to_wav(audio_file_path):
    """
    Konwertuje plik audio do formatu wav, jeśli nie jest już w tym formacie.
    Zwraca ścieżkę do pliku .wav.
    """
    if not audio_file_path.lower().endswith(".wav"):
        try:
            sound = AudioSegment.from_file(audio_file_path)
            wav_file_path = audio_file_path.replace(os.path.splitext(audio_file_path)[1], ".wav")
            sound.export(wav_file_path, format="wav")
            return wav_file_path  # zwracamy sciezke do pliku wav
        except Exception as e:
            print(f"Konwersja audio nie powiodła się, używam oryginalnego pliku : {e}")
            return audio_file_path # zwraca oryginalny plik w razie niepowodzenia
    return audio_file_path # zwraca oryginalny plik jeżeli ma poprawne rozszerzenie

def summarize_with_cohere(text):
    """
    Podsumowuje tekst za pomocą Cohere API.
    """
    try:
        COHERE_API_KEY = os.getenv("COHERE_API_KEY")
        # Inicjalizacja klienta Cohere
        co = cohere.Client(COHERE_API_KEY)
        # Podsumowanie tekstu za pomocą endpointu summarize
        prompt = f"Provide a short summary of the key topics discussed in this online meeting: {text}"
        response = co.generate(
            model="command-r-plus-08-2024",  
            prompt=prompt,
            max_tokens=1000  #
        )
        return response.generations[0].text
    except Exception as e:
        return f"Error in summarization: {str(e)}"
    
def process_audio_to_text(audio_file_path):
    """
    Przetwarza plik audio na tekst przy użyciu modelu Whisper.
    """
    try:
        audio_file_path = _convert_to_wav(audio_file_path)

        # Załaduj model Whisper
        model = whisper.load_model("medium")  # Możesz wybrać "tiny", "base", "small", "medium", "large"
        
        # Transkrypcja audio
        result = model.transcribe(audio_file_path, language='pl')

        summary = summarize_with_cohere(result["text"])
        print(f"Podsumowanie: {summary}")

        # Zapisz transkrypcję w bazie danych
        try:
            last_meeting = Meetings.query.order_by(Meetings.meeting_id.desc()).first()
            if last_meeting:
                meeting_id = str(last_meeting.meeting_id)
            else:
                return jsonify({'error': 'No meeting found in database'}), 404
        except Exception as e:
            return jsonify({'error': f'Failed to fetch last meeting ID: {str(e)}'}), 500
        
        created_at= datetime.now()
        new_transcription = Transcriptions(meeting_id=meeting_id, full_text=result["text"], summary=summary, created_at=created_at)
        db.session.add(new_transcription)
        db.session.commit()

        return result["text"]
    except Exception as e:
        return f"Error in audio processing: {str(e)}"

def process_audio_to_text_google(audio_file_path):
    try:
        audio_file_path = _convert_to_wav(audio_file_path)

        # Użycie SpeechRecognition
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = r.record(source)
        
        # Transkrypcja za pomocą Google Web Speech API
        try:
            text = r.recognize_google(audio_data, language="pl-PL")  # Polish language
        except sr.UnknownValueError:
            return "Google Web Speech API could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Web Speech API; {e}"
        
        return text
    except Exception as e:
        return f"Error in audio processing: {str(e)}"