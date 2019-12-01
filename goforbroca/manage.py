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
    from goforbroca.extensions import db
    from goforbroca.models.languages import Languages

    click.echo("seeding data")

    languages_seed_data = [
        {'name': '한국어'},
        {'name': '汉语'},
    ]

    for seed_data in languages_seed_data:
        language = Languages(**seed_data)
        db.session.add(language)
    db.session.commit()

    click.echo("done seeding data")


if __name__ == "__main__":
    cli()
