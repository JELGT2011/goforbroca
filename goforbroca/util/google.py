from google.cloud import texttospeech

tts_client = texttospeech.TextToSpeechClient()
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)


def text_to_speech(text: str, language_code: str) -> bytes:
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
    )

    audio_content = tts_client.synthesize_speech(synthesis_input, voice, audio_config).audio_content
    return audio_content
