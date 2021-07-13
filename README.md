# Pokémon Trainer API

Project for studying purposes using FastAPI.

# Installing

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


# Known Issues

## Psycopg dependencies

- Problem: pipenv was unable to install `psycopg2` or `psycopg-binary`.
- Solution found: install missing dependency
```sh
sudo apt-get install libpq-dev
```