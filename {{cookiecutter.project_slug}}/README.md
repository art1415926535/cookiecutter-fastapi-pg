# {{cookiecutter.project_name}}


# Production
1. Set up environment variables.

2. Install pip tools:
```
pip install pip-tools
```

3. Install requirements:
```
pip-sync requirements/base.txt
```


# Development
## Setup
### Local
1. Install pip tools:
```
pip install pip-tools
```

2. Install requirements:
```
pip-sync requirements/dev.txt
```

3. Add `.env` file. Example:
```
LOG_LEVEL=debug
LOG_TYPE=console
LOG_TIME_ISO_FORMAT=true
LOG_UTC=false

UVICORN_ACCESS_LOG=true
FASTAPI_DEBUG=true
DOCS_ENABLED=true

POSTGRES_PASSWORD=mysecretpassword
PG_DSN=postgresql://postgres:${POSTGRES_PASSWORD}@127.0.0.1:5432/postgres
```

4. Create database:
```
docker-compose -f deployments/docker-compose.dev.yml --project-directory . up -d db
```

### Docker
1. Add `.env` file. Example:
```
LOG_LEVEL=debug
LOG_TYPE=console
LOG_TIME_ISO_FORMAT=true
LOG_UTC=false

UVICORN_ACCESS_LOG=true
FASTAPI_DEBUG=true
DOCS_ENABLED=true

POSTGRES_PASSWORD=mysecretpassword
PG_DSN=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/postgres
```

2. Run project:
```
docker-compose -f deployments/docker-compose.dev.yml --project-directory . up
```

## Update requirements
1. Add new package to `requirements/base.in` or `requirements/dev.in`.

2. Run:
```
pip-compile --generate-hashes --output-file requirements/base.txt requirements/base.in
pip-compile --generate-hashes --output-file requirements/dev.txt requirements/dev.in
```

3. Update your dev environment: `pip-sync requirements/dev.txt`


# Commands
## Help
```
python -m {{cookiecutter.project_slug}} --help
```

## Serve
```
python -m {{cookiecutter.project_slug}} serve
```

## Code Quality
### Format source code
```
python -m {{cookiecutter.project_slug}} fmt
```

### Run linters
```
python -m {{cookiecutter.project_slug}} lint
```

## Database
### Make migration
```
python -m {{cookiecutter.project_slug}} makemigrations _message_
```

### Run upgrade migration
```
python -m {{cookiecutter.project_slug}} migrate upgrade
```

### Run downgrade migration
```
python -m {{cookiecutter.project_slug}} migrate downgrade -r "-1"
```

## Run tests
```
python -m {{cookiecutter.project_slug}} test
```
or `pytest`