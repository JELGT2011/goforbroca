"""backfill standard_deck source

Revision ID: 0ca581667816
Revises: d79872842061
Create Date: 2020-03-04 18:58:15.044405

"""
from goforbroca.extensions import db
from goforbroca.models.deck import StandardDeck

# revision identifiers, used by Alembic.
revision = '0ca581667816'
down_revision = 'd79872842061'
branch_labels = None
depends_on = None


def upgrade():
    for standard_deck in StandardDeck.query.all():
        if not standard_deck.name.startswith('1000mostcommonwords.com'):
            continue

        standard_deck.name, standard_deck.source = standard_deck.name.split()
        db.session.add(standard_deck)

    db.session.commit()


def downgrade():
    for standard_deck in StandardDeck.query.all():
        if not standard_deck.source == '1000mostcommonwords.com':
            continue

        standard_deck.name = f'1000mostcommonwords.com {standard_deck.name}'
        db.session.add(standard_deck)

    db.session.commit()
