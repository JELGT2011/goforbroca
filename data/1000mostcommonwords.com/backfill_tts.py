import csv
import hashlib
from glob import glob
from io import BytesIO
from os import path
from typing import List, Tuple, Optional

from goforbroca.app import create_app
from goforbroca.models.language import Language
from goforbroca.util.aws import upload_fileobj_to_s3
from goforbroca.util.google import text_to_speech

here = path.realpath(__file__)
data_dir = path.realpath(path.join(here, path.pardir))


def upload_tts(csv_path: str, limit: int = 1000) -> Optional[List[Tuple[str, str, str, str]]]:
    results = list()

    base_name = csv_path.split(path.sep)[-1]
    language_name = path.splitext(base_name)[0]
    language = Language.query.filter_by(name=language_name).scalar()
    if language is None:
        print(f'expected valid language name, instead got {language_name}')
        return

    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    if len(data[0]) != 3:
        print(f'expected row to be of length 3, instead got {data[0]}')
        return

    for row in data[:limit]:
        rank, front, back = row
        audio_content = text_to_speech(front, language.locale)
        m = hashlib.md5()
        m.update(audio_content)
        key = m.hexdigest()
        audio_path = upload_fileobj_to_s3(f'{language.locale}/{key}.mp3', BytesIO(audio_content))
        results += [(*row, audio_path)]

    return results


def backfill_tts(csv_path, data):
    if not data:
        return

    csv_name, ext = path.splitext(csv_path)
    with open(f'{csv_name}_with_audio.{ext}', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for datum in data:
            writer.writerow(datum)


def main():
    app = create_app()
    app.app_context().push()

    for csv_file in glob(f'{data_dir}/*.csv'):
        data = upload_tts(csv_file)
        backfill_tts(csv_file, data)


if __name__ == '__main__':
    main()
