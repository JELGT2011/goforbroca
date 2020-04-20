import hashlib
from io import BytesIO

from goforbroca.util.aws import upload_fileobj_to_s3
from goforbroca.util.google import text_to_speech


def translate_flashcard(text: str, locale: str) -> str:
    audio_content = text_to_speech(text, locale)

    m = hashlib.md5()
    m.update(audio_content)
    key = m.hexdigest()

    audio_path = upload_fileobj_to_s3(f'{locale}/{key}.mp3', BytesIO(audio_content))
    return audio_path
