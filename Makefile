# DEVELOPMENT

dev-install:
	virtualenv -p python3 .venv
	.venv/bin/pip3 install -r requirements.txt
	make dev-path-install

dev-path-install:
	$(foreach dir, $(wildcard .venv/lib/*), echo $(shell pwd)/api > $(dir)/site-packages/grenouilleapi.pth &&) echo

dev-run:
	.venv/bin/python3 api/app.py

dev-clean:
	rm -rf .venv

# DATABASE

db-docker-start:
	docker-compose -p grenouilleapi -f docker/docker-compose.yml up --build -d grenouilleapi_postgres

db-docker-stop:
	docker-compose -p grenouilleapi -f docker/docker-compose.yml down

db-upgrade:
	FLASK_APP=api/app.py .venv/bin/flask db upgrade --directory api/migrations

db-downgrade:
	FLASK_APP=api/app.py .venv/bin/flask db downgrade --directory api/migrations

db-migrate: db-upgrade
	FLASK_APP=api/app.py .venv/bin/flask db migrate --directory api/migrations

# Prod

prod-start:
	# TODO

prod-stop:
	# TODO
