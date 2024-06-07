FROM python:3.11

WORKDIR /workdir
ENV PYTHONPATH "${PYTHONPATH}:/workdir/app"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

RUN pip install poetry

COPY app ./app
COPY migrations ./migrations
COPY ./alembic.ini .
COPY ./pyproject.toml .
COPY ./gunicorn.conf.py .

RUN poetry install --only main --no-root --no-interaction --no-ansi \
  && rm -rf "./.cache"

EXPOSE 8080
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["gunicorn", "--config", "./gunicorn.conf.py", "app.main:app"]