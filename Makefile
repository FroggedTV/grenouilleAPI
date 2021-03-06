# DEVELOPMENT

dev-install:
	virtualenv -p python3 .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install -r backend/requirements.txt
	make dev-path-install

dev-path-install:
	$(foreach dir, $(wildcard .venv/lib/python3.*), echo $(shell pwd)/backend > $(dir)/site-packages/grenouilleapi.pth &&) echo

dev-run:
	.venv/bin/python3 backend/app.py

dev-botrun:
	.venv/bin/python3 backend/bot_app.py

SCRIPT?=hello_world
dev-script:
	.venv/bin/python3 backend/scripts.py $(SCRIPT)

dev-clean:
	rm -rf .venv

# DATABASE

db-docker-start:
	docker-compose -p grenouille -f docker/docker-compose.yml up --build -d grenouilleapi_postgres

db-docker-stop:
	docker-compose -p grenouille -f docker/docker-compose.yml down

db-docker-upgrade:
	docker run -e PYTHONPATH=$PYTHONPATH:/grenouille/backend/ -e FLASK_APP=grenouille/backend/app.py --network host grenouilleapi flask db upgrade --directory grenouille/backend/migrations

db-docker-downgrade:
	docker run -e PYTHONPATH=$PYTHONPATH:/grenouille/backend/ -e FLASK_APP=grenouille/backend/app.py --network host grenouilleapi flask db downgrade --directory grenouille/backend/migrations

db-upgrade:
	FLASK_APP=backend/app.py .venv/bin/flask db upgrade --directory backend/migrations

db-downgrade:
	FLASK_APP=backend/app.py .venv/bin/flask db downgrade --directory backend/migrations

db-migrate: db-upgrade
	FLASK_APP=backend/app.py .venv/bin/flask db migrate --directory backend/migrations

# PROD

build:
	docker-compose -p grenouille -f docker/docker-compose.yml build

prod-start:
	docker-compose -p grenouille -f docker/docker-compose.yml up --build -d

prod-stop:
	docker-compose -p grenouille -f docker/docker-compose.yml down

SCRIPT?=hello_world
prod-script:
	docker run --network host -e FLASK_APP=grenouille/backend/app.py grenouilleapi python3 grenouille/backend/scripts.py $(SCRIPT)

# DOCS
refresh-docs:
	apidoc -i backend/routes -o backend/docs/
