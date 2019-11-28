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
pip install requirements-dev.txt
pytest
```

### Installing a wsgi server

This project provide a simple wsgi entry point to run gunicorn or uwsgi for example.

#### Running with gunicorn

For gunicorn you only need to run the following commands.

```bash
pip install gunicorn
gunicorn goforbroca.wsgi:app
```

#### Running with uwsgi

Pretty much the same as gunicorn here.

```bash
pip install uwsgi
uwsgi --http 127.0.0.1:5000 --module goforbroca.wsgi:app
```

### Using Flask CLI

This cookiecutter is fully compatible with default flask CLI and use a `.flaskenv` file to set correct env variables to bind the application factory.
Note that we also set `FLASK_ENV` to `development` to enable debugger.


### Using Celery

This code will include a dummy task located in `goforbroca/goforbroca/tasks/example.py` that only return `"OK"` and a `celery_app` file used to your celery workers.


#### Running celery workers

```bash
celery worker -A goforbroca.celery_app:app --loglevel=info
```

If you have updated your configuration for broker/result backend your workers should start and you should see the example task available.

```
[tasks]
  . goforbroca.tasks.example.dummy_task
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
