# Pokémon Trainer API

Project for studying purposes using FastAPI.

# Installing

Make sure your `.env` file is configured with:
```
DB
DB_NAME
DB_USER
DB_PSWD
DB_HOST
DB_PORT

SECRET_KEY
```

* You can generate a new `SECRET_KEY` with
```sh
openssl rand -hex 32
```

## Install Using Pipenv

Make sure you have pipenv installed:
```sh
pip install pipenv
```
Install dependencies:
```sh
pipenv install
```
Enter the virtual env.:
```sh
pipenv shell
```
Start the server:
```
uvicorn app.main:app
```

## Install Using Docker

Build the docker image
```
docker-compose build
```

Run the containers
```
docker-compose up
```

The server will be listening at [localhost:8000](http://localhost:8000).

Check both `Dockerfile` and `docker-compose.yml` for further documentation.

# Testing

You can test inside the container, on the postgres database, using
```
docker-compose run --rm --no-deps --entrypoint=pytest app /tests
```

To test locally using sqlite, add the following line to `.env`:
```
TESTING_DB_URL=sqlite:///testing.db
```

And then everything you run locally (the app or pytest) will use the local sqlite database (`./testing.db`).

> If you consider usefull, you can also run only the postgres database container using
> ```
> docker-compose up -d postgres
> ```

# Other commands

Other useful commands are specified at `Makefile`.

# Known Issues

## Psycopg dependencies

- Problem: pipenv was unable to install `psycopg2` or `psycopg-binary`.
- Solution found: install missing dependency
```sh
sudo apt-get install libpq-dev
```