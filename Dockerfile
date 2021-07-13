FROM python:3.8-buster

RUN pip install pipenv

COPY Pipfile /
COPY Pipfile.lock /
RUN pipenv install --system --deploy

COPY app/ /app/
COPY core/ /core/
COPY populate.py /
COPY setup.sh /

WORKDIR /
CMD ./setup.sh