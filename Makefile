run-dev:
	poetry run python manage.py runserver

run-polling:
	poetry run python run_polling.py

build-latest:
	docker build --tag=korablinbot:latest .

run-docker:
	docker run \
		--name=korablinbot \
		--rm \
		--env-file ./.env \
		-it \
		-p 8000:8000 \
		korablinbot:latest

run-docker-dev:
	docker run \
		--name=korablinbot \
		--rm \
		--env-file ./dev.env \
		-it \
		-p 8000:8000 \
		korablinbot:latest

run-redis:
	docker run --rm --name=redis -d -p 6379:6379 redis

stop-redis:
	docker stop redis

run-celery:
	poetry run celery -A app worker -l DEBUG -P eventlet

stop-docker:
	docker stop korablinbot

connect-container:
	docker exec -it korablinbot bash