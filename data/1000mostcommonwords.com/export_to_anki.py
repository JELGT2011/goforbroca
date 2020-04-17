import csv
from glob import glob
from os import path
from random import randrange
from typing import List

import genanki

from goforbroca.app import create_app
from goforbroca.models.language import Language
from goforbroca.util.aws import download_fileobj_from_s3, bucket_url

here = path.realpath(__file__)
data_dir = path.realpath(path.join(here, path.pardir))
media_dir = path.join(data_dir, 'media')


def get_media_files(csv_path: str, limit: int = 1000) -> List[str]:
    results = list()

    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    for rank, front, back, audio_url in data[:limit]:
        key = audio_url[len(bucket_url) + 1:]  # + 1 for the trailing '/'
        output_path = path.join(media_dir, key)
        results += [output_path]

    return results


def download_media_files(csv_path: str, limit: int = 1000) -> List[str]:
    results = list()

    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    for rank, front, back, audio_url in data[:limit]:
        key = audio_url[len(bucket_url) + 1:]  # + 1 for the trailing '/'
        output_path = path.join(media_dir, key)
        download_fileobj_from_s3(key, output_path)
        results += [output_path]

    return results


def export_from_csv(csv_path: str, media_files: List[str], limit: int = 1000):
    base_name = csv_path.split(path.sep)[-1]
    language_name = path.splitext(base_name)[0]
    language = Language.query.filter_by(name=language_name).scalar()
    if language is None:
        print(f'expected valid language name, instead got {language_name}')
        return

    anki_name = f'1000mostcommonwords.com {language_name}'
    model = genanki.Model(
        randrange(1 << 30, 1 << 31),
        anki_name,
        fields=[{'name': name} for name in ['Rank', 'Front', 'Back', 'Audio']],
        templates=[
            {
                'name': 'Front -> Back',
                'qfmt': '{{Front}}<br>{{Audio}}',
                'afmt': '{{Back}}',
            },
            {
                'name': 'Back -> Front',
                'qfmt': '{{Back}}',
                'afmt': '{{Front}}<br>{{Audio}}',
            },
            {
                'name': 'Audio -> Text',
                'qfmt': '{{Audio}}',
                'afmt': '{{Front}}<br>{{Back}}',
            },
        ],
    )

    deck = genanki.Deck(randrange(1 << 30, 1 << 31), anki_name)

    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    for (rank, front, back, audio_url), audio in zip(data[:limit], media_files[:limit]):
        note = genanki.Note(model=model, fields=[rank, front, back, f'[sound:{audio}]'])
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(f'{anki_name}.apkg')


def main():
    app = create_app()
    app.app_context().push()

    for csv_file in glob(f'{data_dir}/*.csv'):
        media_files = get_media_files(csv_file)
        export_from_csv(csv_file, media_files)


if __name__ == '__main__':
    main()
