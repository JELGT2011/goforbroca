from goforbroca.extensions import celery, db
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition


@celery.task
def learn():
    user_decks = UserDeck.filter_by(active=True)
    for user_deck in user_decks:
        last_repetition = (db.session.query(Repetition)
                           .filter_by(deck_id=user_deck.id)
                           .order_by(Repetition.completed_at.desc()).scalar())
        if not last_repetition:
            # get lowest rank flashcard in the deck
            flashcard = db.session.query(Flashcard).filter_by(deck_id=user_deck.id).order_by(Flashcard.rank.asc()).scalar()
            if not flashcard:
                # user is done with this deck
                user_deck.active = False
                user_deck.save()
                continue
        else:
            flashcard = db.session.query(Flashcard).get(last_repetition.flashcard_id)

        # TODO: create new repetition from flashcard
    return "OK"
