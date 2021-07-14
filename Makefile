all: build up test down

buildup: build up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

test:
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests