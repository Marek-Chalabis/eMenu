FROM python:3.9.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
RUN addgroup -S app && adduser -S app -G app
# app directory
RUN mkdir /app
ENV APP_HOME=/app
WORKDIR $APP_HOME

# psycopg2-binary packages requirment
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependecies
RUN pip install --upgrade pip
COPY requirements.txt /.
RUN pip install -r /requirements.txt

# TODO add lints here or on CI/CD

# copy entrypoint.sh for prod or develop
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

# copy project
COPY ./ $APP_HOME

# create app user and give him permissions

RUN chown -R app:app $APP_HOME
USER app

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]