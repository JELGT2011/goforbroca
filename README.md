### API

```bash
export HOST=https://goforbroca-backend.herokuapp.com
export GOOGLE_AUTH_TOKEN=...
```

User operations
```bash
# create user
curl "{HOST}/api/users/" \
    --request "POST" \
    --header "content-type: application/json" \
    --header "accept: application/json" \
    --header "authorization: bearer ${GOOGLE_AUTH_TOKEN}" \
        | jq '.'

# get user
curl "{HOST}/api/users/" \
    --request "GET" \
    --header "content-type: application/json" \
    --header "accept: application/json" \
    --header "authorization: bearer ${GOOGLE_AUTH_TOKEN}" \
        | jq '.'
```

```bash
# Deck
get standard decks: `GET /api/decks/standard`
get user decks: `GET /api/decks/user`
fork standard deck: `POST /api/decks/standard/<standard_deck_id>/fork`
create user deck: `POST /api/decks/user` `{"name": String}`
delete user deck: `DELETE /api/decks/user/<user_deck_id>`
```

### Installation

```bash
pip install -r requirements.txt
pip install -e .
```

You have now access to cli commands and you can init your project.

```bash
goforbroca init
```

To list all commands:
```bash
goforbroca --help
```

### Configuration

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

#### Running celery workers

```bash
celery worker -A goforbroca.celery_app:app --loglevel=info
```

#### Running a task

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
