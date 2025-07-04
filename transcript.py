import assemblyai as aai
import requests
GEMINI_API_KEY = "AIzaSyAQYaGBFQKw0DF1Ixyzn-wrpXB0_j5r-DE"

aai.settings.api_key = "e2998b1ada764da98d7a0cf4c6d4247f"


BASIC_QUERY = "Donne moi les 3 thèmes de la journées proposé dans ce texte. et donne moi le thème selectionné par le joueur, Si tu n'arrive a faire ni l un ni 'autre, juste output '?' sinon output juste et sans rien dire d'autre le thème selectionné "


def transcirbe_audio(audio_file_path) -> str:
    """
    Transcribes the given audio file using the AssemblyAI API with French language settings.
    Args:
        audio_file_path (str): The file path to the audio file to be transcribed.
    Returns:
        str: The transcribed text if transcription is successful, or "NULL" if an error occurs.
    Side Effects:
        Prints the status and result of the transcription process.
    """
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.universal,
                                    language_code=aai.LanguageCode.fr,)

    transcript = transcriber.transcribe(audio_file_path, config)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
        return "NULL"
    elif transcript.status == aai.TranscriptStatus.completed:
        
        return transcript.text








def ask_gemini(prompt, api_key):
    """
    Sends a prompt to the Gemini API and returns the generated response text.

    Args:
        prompt (str): The input prompt to send to the Gemini model.
        api_key (str): The API key for authenticating with the Gemini API.

    Returns:
        str: The generated response text from the Gemini model, or "NULL" if the response is invalid or missing.

    Raises:
        requests.HTTPError: If the HTTP request to the Gemini API fails.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    # Extract the answer from the response
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "NULL"




def get_daily_themes(file_path: str) -> str:
    """
    Retrieves the daily themes from the Gemini API.

    Returns:
        str: The daily themes as a string, or "NULL" if an error occurs.
    """
    transcript = transcirbe_audio(file_path)
    response = ask_gemini(BASIC_QUERY+ transcript, GEMINI_API_KEY)
    return response




print(get_daily_themes("03-07-2025.mp3"))