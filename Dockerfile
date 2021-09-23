FROM python:3.9-alpine3.13

LABEL maintainer="lomank200222@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./placerem /placerem
COPY ./scripts /scripts

WORKDIR /placerem

# Heroku won't use this
#EXPOSE 8000

# libffi-dev, openssl-dev, cargo - for cryptography - for social-auth-app-django, social-auth-core
# jpeg-dev, libjpeg-dev zlib-dev - for easy-thumbnails

RUN apk add --update --no-cache nodejs npm && \
    # Installing npm packages
    npm ci && \
    npm run prod && \
    npm prune --production && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base jpeg-dev postgresql-dev musl-dev linux-headers \
        zlib-dev libffi-dev openssl-dev python3-dev cargo && \
    apk add --update --no-cache libjpeg && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home placerem && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R placerem:placerem /vol && \
    # Or you'll get permission denied error
    chown -R placerem:placerem /py/lib/python3.9/site-packages/social_django/migrations && \
    chown -R placerem:placerem /py/lib/python3.9/site-packages/easy_thumbnails/migrations && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER placerem

CMD ["run.sh"]