FROM python:3.8.6-buster

ARG GIT_HASH=dev
ENV GIT_HASH=$GIT_HASH

ARG REQUIREMENTS_FILE=base.txt

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install pip-tools

WORKDIR /app
RUN useradd -m -r user && \
    chown user /app

COPY requirements/$REQUIREMENTS_FILE requirements/$REQUIREMENTS_FILE
RUN pip-sync requirements/$REQUIREMENTS_FILE

COPY . .

USER user

ENTRYPOINT ["python", "-m", "{{cookiecutter.project_slug}}"]
