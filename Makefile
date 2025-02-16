# Variabili
PYTHON = python3
ALEMBIC = alembic
APP = src.api.api:app

.PHONY: install migrate test run clean

# Installazione dipendenze
install:
	pip install -r requirements.txt

# Comandi Database/Alembic
db-init:
	$(ALEMBIC) init migrations

migrate-create:
	$(ALEMBIC) revision --autogenerate -m "$(name)"

migrate-up:
	$(ALEMBIC) upgrade head

migrate-down:
	$(ALEMBIC) downgrade -1

migrate-reset:
	$(ALEMBIC) downgrade base

# Avvio applicazione
run:
	uvicorn $(APP) --reload