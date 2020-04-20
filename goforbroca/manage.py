from glob import glob
from os import path

import click
from flask.cli import FlaskGroup
from sqlalchemy.exc import IntegrityError

from goforbroca.app import create_app


def create_goforbroca(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_goforbroca)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from goforbroca.extensions import db

    click.echo("creating database")
    db.create_all()
    click.echo("done creating database")

    seed_all()


@cli.command("seed_all")
def seed_all():
    seed_languages()
    seed_flashcards()


@cli.command("seed_languages")
def seed_languages():
    from goforbroca.models.language import Language

    click.echo("seeding languages")
    kwargs = [
        {'name': 'english', 'locale': 'en-US'},
        {'name': '한국어', 'locale': 'ko-KR'},
        {'name': '汉语', 'locale': 'cmn-CN'},
        {'name': 'español', 'locale': 'es-ES'},
    ]
    try:
        for k in kwargs:
            Language.create(**k)
    except IntegrityError:
        pass

    click.echo("done seeding languages")


@cli.command("seed_flashcards")
def seed_flashcards():
    seed_1000mostcommonwords_com()


def seed_1000mostcommonwords_com():

    click.echo("seeding 1000mostcommonwords.com")
    for common_words_file in glob('data/1000mostcommonwords.com/*.csv'):
        seed_1000mostcommonwords_com_file(common_words_file)

    click.echo("done seeding 1000mostcommonwords.com")


def seed_1000mostcommonwords_com_file(common_words_file):
    from goforbroca.models.deck import StandardDeck
    from goforbroca.models.flashcard import Flashcard
    from goforbroca.models.language import Language
    from goforbroca.extensions import db

    base_name = common_words_file.split(path.sep)[-1]
    language_name = base_name.split('.')[0]
    language = Language.query.filter_by(name=language_name).scalar()
    if not language:
        print(f'expected valid language name, instead got {language_name}')

    source = '1000mostcommonwords.com'
    click.echo(f"seeding {source}/{language_name}")
    standard_deck = StandardDeck.create(name=language_name, source=source)
    with open(common_words_file) as common_words_csv:
        for line in common_words_csv:
            rank, front, back, audio_url = line.strip().split(',')
            flashcard = Flashcard(
                language_id=language.id,
                standard_deck_id=standard_deck.id,
                front=front,
                back=back,
                rank=rank,
                audio_url=audio_url,
                refresh_at=None,
            )
            db.session.add(flashcard)
        db.session.commit()


if __name__ == "__main__":
    cli()
