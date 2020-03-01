### API

```bash
export GOOGLE_AUTH_TOKEN=...
```

```bash
# create user
curl "localhost:5000/api/users/" \
    --request "POST" \
    --header "content-type: application/json" \
    --header "accept: application/json" \
    --header "authorization: bearer ${GOOGLE_AUTH_TOKEN}" \
        | jq '.'

# get user
curl "localhost:5000/api/users/" \
    --request "GET" \
    --header "content-type: application/json" \
    --header "accept: application/json" \
    --header "authorization: bearer ${GOOGLE_AUTH_TOKEN}" \
        | jq '.'

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
