FROM python:3.11-slim

RUN apt update && apt install python3 netcat -y curl && rm -rf /var/cache/apt/* /var/lib/apt/lists/*

ENV PYTHONPATH "=${PYTHONPATH}:${APP_HOME}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV APP_HOME="/home/app"
ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY pyproject.toml poetry.lock $APP_HOME
RUN pip install poetry==1.3.2
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root

COPY . $APP_HOME

RUN chmod +x /home/app/entrypoint.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]