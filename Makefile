# Load environment variables from .env file
include .env
export $(shell sed 's/=.*//' .env)

# Variables
VENV_NAME = venv

# Create and activate virtual environment
.PHONY: venv
venv:
	python -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install -r requirements.txt

# Install Python dependencies
.PHONY: install
install:
	$(VENV_NAME)/bin/pip install Flask==2.0.3 Flask-Migrate==3.1.0 Flask-SQLAlchemy==2.5.1 Werkzeug==2.0.3



# Start only the database container
.PHONY: docker-run-only-db
docker-run-only-db:
	docker-compose -f docker-compose-db.yaml up -d

# Initialize Flask-Migrate
.PHONY: db-init
db-init:
	$(VENV_NAME)/bin/flask db init

# Create migration
.PHONY: db-migrate
db-migrate:
	@read -p "Enter migration message: " message; \
	$(VENV_NAME)/bin/flask db migrate -m "$$message"

# Apply migration
.PHONY: db-upgrade
db-upgrade:
	$(VENV_NAME)/bin/flask db upgrade

# Drop all tables and reapply migration
.PHONY: db-reset
db-reset:
	$(VENV_NAME)/bin/flask db downgrade base
	$(VENV_NAME)/bin/flask db upgrade

# Run the Flask application
.PHONY: run-dev
run:
	python run.py

# Run the Flask application in production mode
.PHONY: run-prod
run-prod:
	$(VENV_NAME)/bin/gunicorn -w 4 -k gevent -b 0.0.0.0:5000 app:app



.PHONY: test
test:
	$(VENV_NAME)/bin/pytest --cov=app tests