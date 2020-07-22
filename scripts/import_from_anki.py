from glob import glob
from os import path
from typing import List, Tuple

from goforbroca.app import create_app
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard

here = path.realpath(__file__)
root_dir = path.realpath(path.join(here, path.pardir))
temp_dir = path.join(root_dir, 'temp')


def import_from_anki(anki_file_path: str) -> Tuple[UserDeck, List[Flashcard]]:
    pass


def export_to_csv(anki_file_path: str, deck: UserDeck, flashcards: List[Flashcard]):
    base_name = anki_file_path.split(path.sep)[-1]
    language_name = path.splitext(base_name)[0]


def main():
    app = create_app()
    app.app_context().push()

    for anki_file in glob(path.join(temp_dir, '*.txt')):
        deck, flashcards = import_from_anki(anki_file)
        export_to_csv(anki_file, deck, flashcards)


if __name__ == '__main__':
    """
    Usage: `psql < import_from_anki.psql`
    """
    main()
