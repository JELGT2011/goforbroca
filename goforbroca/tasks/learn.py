from textwrap import dedent

from goforbroca.extensions import celery
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition
from goforbroca.models.user import User
from goforbroca.tasks.review import review


@celery.task
def learn():
    user_decks = UserDeck.filter_by(active=True)
    for user_deck in user_decks:
        user = User.query.get(user_deck.user_id)
        last_repetition = (Repetition.query
                           .filter_by(user_deck_id=user_deck.id)
                           .order_by(Repetition.completed_at.desc())
                           .scalar())
        if not last_repetition:
            # get lowest rank flashcard in the deck
            flashcard = Flashcard.query.filter_by(deck_id=user_deck.id).order_by(Flashcard.rank.asc()).scalar()
            if not flashcard:
                # user is done with this deck
                user_deck.active = False
                user_deck.save()
                continue
        else:
            flashcard = Flashcard.query.get(last_repetition.flashcard_id)

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

        # TODO
        # client.messages.create(
        #     body=message,
        #     to=user.phone_number,
        # )

    return True
