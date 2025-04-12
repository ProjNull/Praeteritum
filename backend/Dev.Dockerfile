FROM python:3.11.8 AS pre

WORKDIR /opt/prae-be

RUN python -m pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry export --without-hashes --format requirements.txt --output requirements.txt

FROM python:3.11.8 AS prod

WORKDIR /opt/prae-be

COPY --from=pre /opt/prae-be/requirements.txt .
COPY app ./app

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
