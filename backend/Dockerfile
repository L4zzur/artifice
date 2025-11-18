ARG ALPINE_VERSION=3.22
ARG PYTHON_VERSION=3.13.7
ARG PYTHON_TAG=${PYTHON_VERSION}-alpine${ALPINE_VERSION}
ARG UV_TAG=alpine${ALPINE_VERSION}


FROM ghcr.io/astral-sh/uv:${UV_TAG} AS uv_tool


FROM python:${PYTHON_TAG} AS dependencies
WORKDIR /app
COPY ./uv.lock ./pyproject.toml ./
COPY --from=uv_tool /usr/local/bin/uv /bin/
RUN uv export --format requirements-txt --no-hashes --no-dev -o ./requirements.txt


FROM python:${PYTHON_TAG}
WORKDIR /app
RUN apk add --no-cache build-base
COPY --from=dependencies /app/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache -r ./requirements.txt
COPY . .
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

EXPOSE 8000


#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]