FROM python:3.11.2-slim

ENV POETRY_HOME="/opt/poetry"

RUN pip install --upgrade pip
RUN pip install poetry
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

RUN mkdir -p /app
COPY . /app

WORKDIR /app

RUN poetry install --without dev

CMD ["poetry", "run", "hashtag-bot"]