import click
from flask.cli import FlaskGroup

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

    seed()


@cli.command("seed")
def seed():
    click.echo("seeding data")
    seed_languages()
    seed_1000mostcommonwords_com()
    click.echo("done seeding data")


def seed_languages():
    from goforbroca.models.languages import Languages
    seed_data = [
        {'name': 'english'},
        {'name': '한국어'},
        {'name': '汉语'},
    ]
    Languages.bulk_create(seed_data)


def seed_1000mostcommonwords_com():
    from goforbroca.models.languages import Languages
    from goforbroca.models.words import Words
    from goforbroca.models.translations import Translations
    languages = [language for language in Languages.all() if language.name != 'english']
    english = Languages.get_by_name('english')
    for language in languages:
        with open(f'data/1000mostcommonwords.com/{language.name}.csv') as language_csv:
            for line in language_csv:
                rank, from_name, to_name = line.strip().split(',')
                rank = int(rank)
                from_word = Words.get_by_name(from_name) or Words.create(language_id=language.id, name=from_name)
                to_word = Words.get_by_name(to_name) or Words.create(language_id=english.id, name=to_name)
                Translations.create(from_word_id=from_word.id, to_word_id=to_word.id, rank=rank)


if __name__ == "__main__":
    cli()
