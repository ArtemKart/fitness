ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE := .venv\Scripts\activate
else
    VENV_ACTIVATE := .venv/bin/activate
endif

ifndef ENV_FILE_EXISTS
    ifeq ($(wildcard .env),)
        ENV_FILE_EXISTS := false
    else
        ENV_FILE_EXISTS := true
    endif
endif

.PHONY: install lint run down clean

$(VENV_ACTIVATE): requirements.txt
	python3.11 -m venv .venv
	. $(VENV_ACTIVATE) && pip install --upgrade pip \
	&& pip install -r requirements.txt

install: $(VENV_ACTIVATE)

lint: $(VENV_ACTIVATE)
	. $(VENV_ACTIVATE) && black .

run_docker:
		@if [ "$(ENV_FILE_EXISTS)" = "false" ]; then \
		cp .env-template .env; \
	 fi
		docker compose up -d --build

run_server:
	. $(VENV_ACTIVATE) && uvicorn --reload api.main:app

down:
	docker compose down --volumes