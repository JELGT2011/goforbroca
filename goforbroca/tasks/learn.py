from textwrap import dedent

from twilio.rest import Client

from goforbroca import config
from goforbroca.extensions import celery, db
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition
from goforbroca.models.user import User
from goforbroca.tasks.review import review

client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


@celery.task
def learn():
    user_decks = UserDeck.filter_by(active=True)
    for user_deck in user_decks:
        user = db.session.query(User).get(user_deck.user_id)
        last_repetition = (db.session.query(Repetition)
                           .filter_by(user_deck_id=user_deck.id)
                           .order_by(Repetition.completed_at.desc())
                           .scalar())
        if not last_repetition:
            # get lowest rank flashcard in the deck
            flashcard = (db.session.query(Flashcard)
                         .filter_by(deck_id=user_deck.id)
                         .order_by(Flashcard.rank.asc())
                         .scalar())
            if not flashcard:
                # user is done with this deck
                user_deck.active = False
                user_deck.save()
                continue
        else:
            flashcard = db.session.query(Flashcard).get(last_repetition.flashcard_id)

        new_repetition = Repetition.create(
            user_id=user.id,
            user_deck_id=user_deck.id,
            flashcard_id=flashcard.id,
            iteration=last_repetition.iteration + 1 if last_repetition else 0,
            active=True,
        )
        review.delay()
        message = f"""
            you have a new flashcard today for {user_deck.name}
            front: {flashcard.front}
            back: {flashcard.back}
            let's check back on this soon!
        """
        message = dedent(message)
        client.messages.create(
            body=message,
            from_=config.TWILIO_PHONE_NUMBER,
            to=user.phone_number,
        )

    return True
