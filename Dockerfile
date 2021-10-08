FROM python:3.8-slim

WORKDIR /

RUN pip install pipenv

COPY Pipfile /
COPY Pipfile.lock /
RUN pipenv install --system --deploy

COPY populate.py /
COPY setup.sh /

COPY core/ /core/
COPY tests/ /tests/
COPY app/ /app/

CMD ./setup.sh