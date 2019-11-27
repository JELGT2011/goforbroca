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
    click.echo("create database")
    db.create_all()
    click.echo("done")


if __name__ == "__main__":
    cli()
