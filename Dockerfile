FROM python:3.9.6-alpine

ENV PYTHONUNBUFFERED=1

# app directory
RUN mkdir /app
ENV APP_HOME=/app
WORKDIR $APP_HOME

# linux packages
RUN apk add --no-cache --update \
    postgresql-dev \
    python3-dev \
    libc-dev \
    linux-headers \
    zlib \
    zlib-dev \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    gcc \
    musl-dev \
    libgcc \
    openssl-dev \
    curl \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev tcl-dev


# install dependecies and delete packages not needed after
RUN pip install --upgrade pip
COPY requirements.txt /.
RUN pip install -r /requirements.txt

# TODO add lints here or on CI/CD

# copy project
COPY ./ $APP_HOME

# create app user and give him permissions
RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app $APP_HOME

USER app
