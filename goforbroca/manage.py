from glob import glob

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
    seed_1000mostcommonwords_com()


def seed_1000mostcommonwords_com():
    from goforbroca.models.deck import StandardDeck
    from goforbroca.models.flashcard import Flashcard

    click.echo("seeding 1000mostcommonwords.com")
    for common_words_file in glob('data/1000mostcommonwords.com/*.csv'):
        base_name = common_words_file.split('/')[-1]
        language_name = base_name.split('.')[0]
        deck_name = f'1000mostcommonwords.com {language_name}'
        click.echo(f"\tseeding {deck_name}")
        standard_deck = StandardDeck.create(name=deck_name)
        with open(common_words_file) as common_words_csv:
            for line in common_words_csv:
                rank, front, back = line.strip().split(',')
                rank = int(rank)
                Flashcard.create(standard_deck_id=standard_deck.id, front=front, back=back, rank=rank)
                Flashcard.create(standard_deck_id=standard_deck.id, front=back, back=front, rank=rank)
    click.echo("done seeding 1000mostcommonwords.com")


if __name__ == "__main__":
    cli()
