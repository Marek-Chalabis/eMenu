FROM python:3.9.6-alpine

ENV PYTHONUNBUFFERED=1

# app directory
RUN mkdir /app
ENV APP_HOME=/app
WORKDIR $APP_HOME

# install dependecies and delete packages not needed after
RUN pip install --upgrade pip
COPY requirements.txt /.
RUN apk add --update --no-cache postgresql-dev gcc python3-dev musl-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    libc-dev linux-headers  zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# TODO add lints here or on CI/CD

# copy project
COPY ./ $APP_HOME

# create app user and give him permissions
RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app $APP_HOME

USER app
