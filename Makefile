all: build up test down

buildup: build up

build:
	docker-compose build

up:
	docker-compose up -d

db:
	docker-compose up -d postgres

down:
	docker-compose down --remove-orphans

test:
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests