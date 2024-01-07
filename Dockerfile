FROM python:3.11.2-slim

ENV POETRY_HOME="/opt/poetry"

RUN pip install --upgrade pip
RUN pip install alembic poetry




ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN mkdir -p /app
COPY . /app

WORKDIR /app
RUN groupadd -r mygroup
RUN useradd -r -g mygroup user
RUN chown -R user:mygroup /app
RUN chmod -R 755 /app
RUN chmod -R a+w /app

RUN pip install -r /app/requirements.txt
#
#RUN alembic revision --autogenerate
#RUN alembic upgrade head
#
#RUN poetry build
#RUN poetry install

WORKDIR /app
USER user
ENTRYPOINT ["poetry", "run", "hashtag-bot"]