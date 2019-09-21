FROM python:3.7

WORKDIR /usr/app

ARG FLASK_ENV

ENV FLASK_ENV=${FLASK_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=0.12.17

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /usr/app/

# Project initialization:
RUN poetry config settings.virtualenvs.create false \
    && poetry install $(test X"$FLASK_ENV" = production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /usr/app

ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0"]
