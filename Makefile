# DEVELOPMENT

dev-install:
	virtualenv -p python3 .venv
	.venv/bin/pip3 install -r backend/requirements.txt
	make dev-path-install

dev-path-install:
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd)/backend > $(dir)/site-packages/grenouilleapi.pth &&) echo

dev-clean:
	rm -rf .venv

dev-backend-run:
	.venv/bin/python3 backend/app.py

dev-frontend-run:
	TODO

# DATABASE

db-docker-start:
	docker-compose -p grenouille -f docker/docker-compose.yml up --build -d grenouilleapi_postgres

db-docker-stop:
	docker-compose -p grenouille -f docker/docker-compose.yml down

db-upgrade:
	FLASK_APP=backend/app.py .venv/bin/flask db upgrade --directory backend/migrations

db-downgrade:
	FLASK_APP=backend/app.py .venv/bin/flask db downgrade --directory backend/migrations

db-migrate: db-upgrade
	FLASK_APP=backend/app.py .venv/bin/flask db migrate --directory backend/migrations

# PROD

prod-start:
	docker-compose -p grenouille -f docker/docker-compose.yml up --build -d

prod-stop:
	docker-compose -p grenouille -f docker/docker-compose.yml down

# DOCS
refresh-docs:
	apidoc -i backend/routes -o backend/docs/
