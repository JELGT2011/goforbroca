from typing import Optional

from google.cloud import texttospeech
from google.cloud import translate_v2 as translate

detect_language_min_confidence = 0.8

translate_client = translate.Client()

tts_client = texttospeech.TextToSpeechClient()
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)


def detect_language(text: str) -> Optional[str]:
    response = translate_client.detect_language(text)
    if response['confidence'] < detect_language_min_confidence:
        return None

    return response['language'][:2]


def translate_text(text: str, language_code: str) -> str:
    response = translate_client.translate(text, target_language=language_code)
    return response['translatedText']


def text_to_speech(text: str, locale_or_language_code: str) -> bytes:
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=locale_or_language_code,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
    )

    response = tts_client.synthesize_speech(synthesis_input, voice, audio_config)
    audio_content = response.audio_content
    return audio_content
