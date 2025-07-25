include .env
export

default:
	@echo "Please specify a target to make."
# Export python requirements to requirements.txt
req:
	uv export --format requirements-txt -o requirements.txt --no-hashes --no-dev --no-header
# Migrate database
m:
	cd app &&\
	uv run python manage.py migrate
# Make migrations
mm:
	cd app &&\
	uv run python manage.py makemigrations
# Make migrations and migrate
mmm: mm m
# Drop local database tables
drop-tables:
	psql "dbname=postgres host=db port=5432 user=postgres password=postgres" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" ;\
	exit 0;
# Re-initialize project
init-proj: drop-tables m
# Run hypercorn ASGI server
hypercorn:
	cd app &&\
	python manage.py collectstatic --noinput &&\
	hypercorn app.asgi:application --workers 4 -b 0.0.0.0:8000
# Run hypercorn ASGI server with reload, if you are not using debugger, run gateway using this.
hypercorn-dev:
	cd app &&\
	hypercorn app.asgi:application --reload --workers 4 -b 0.0.0.0:8000
# Run celery worker
run-worker:
	cd app &&\
	uv run celery -A app worker -l INFO -E
# Run celery scheduler
run-beat:
	cd app &&\
	uv run celery -A app beat -l INFO

# FastStream
# Run FastStream worker server
fs-dev:
	cd app &&\
	uv run faststream run serve_faststream:app --reload

# FastAPI WebSocket server
realtime-dev:
	cd app &&\
	uv run fastapi run serve_fastapi.py --port 8080 --reload