# DEVELOPMENT

dev-backend-install:
	virtualenv -p python3 .venv
	.venv/bin/pip3 install -r backend/requirements.txt
	make dev-path-install

dev-path-install:
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd)/backend > $(dir)/site-packages/grenouilleapi.pth &&) echo

dev-backend-run:
	.venv/bin/python3 backend/app.py

dev-backend-clean:
	rm -rf .venv

dev-frontend-install:
	cd frontend && npm install

dev-frontend-run:
	cd frontend && npm run dev

dev-frontend-unit:
	cd frontend && npm run unit

dev-frontend-teste2e:
	cd frontend && npm run e2e

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
