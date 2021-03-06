## API

```bash
export HOST=https://goforbroca-backend.herokuapp.com
export GOOGLE_AUTH_TOKEN=...
```

```
User
create user: `POST /api/users` `{"email": String}`

get user: `GET /api/users`

update user: `PUT` `{}`  # TODO: not implemented
```

```
Deck
get standard decks: `GET /api/decks/standard`

get user decks: `GET /api/decks/user`

fork standard deck: `POST /api/decks/standard/<standard_deck_id>/fork`

create user deck: `POST /api/decks/user` `{"name": String, "active": Optional[Boolean] = True}`

update user deck: `PUT /api/decks/user/<user_deck_id>` `{"name": Optional[String], "active": Optional[Boolean]}`

delete user deck: `DELETE /api/decks/user/<user_deck_id>`
```

```
Flashcard
list cards: `GET /api/flashcards` `{"page_number": Optional[Int], "page_size": Optional[Int], "standard_deck_id": Optional[Int], "user_deck_id": Optional[Int]}`

create card: `POST /api/flashcards` `{"language_id": Optional[Int], "user_deck_id": Optional[Int], "front": String, "back": Optional[String], "rank": Optional[Int]}`

update card: `PUT /api/flashcards/<flashcard_id>` `{"front": Optional[String], "back": Optional[String], "rank": Optional[Int]}`

delete card: `DELETE /api/flashcards/<flashcard_id>`

view new card: `POST /api/flashcards/view` `{"user_deck_id": Optional[Int]}`
```

```
Repetition
create repetition: `POST /api/repetitions` `{"user_deck_id": Optional[Int]}`
submit repetition: `POST /api/repetitions/<repetition_id>` `{"score": Int}`
```

### Installation

```bash
pip install -r requirements.txt
pip install -e .
```

You now have access to cli commands and you can init your project.

```bash
goforbroca init
```

To list all commands:
```bash
goforbroca --help
```

## Configuration

Configuration is handled by environment variables, for development purpose you just need to update/add entries in `.flaskenv` file.

```bash
cp .flaskenv.template .flaskenv
```

### Running tests

```bash
pip install -r requirements-dev.txt
```

#### Running with gunicorn

```bash
gunicorn goforbroca.wsgi:app
```

### Running celery workers

```bash
celery worker -A goforbroca.celery_app:app --loglevel=info
```

### Running a task

To run a task you can either import it and call it

```python
from goforbroca.tasks.example import dummy_task
result = dummy_task.delay()
result.get()
'OK'
```

Or use the celery extension

```python
from goforbroca.extensions import celery
celery.send_task('goforbroca.tasks.example.dummy_task').get()
'OK'
```

## Heroku

```bash
heroku run bash --app=goforbroca-backend
```
