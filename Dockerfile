FROM python:3.8.10
LABEL maintainer="beyztodo.com"

ENV PYTHONUNBUFFERED 1 # consola basması için


COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8002

RUN apt update
RUN ["apt-get", "update"]
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home\
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user