FROM python:3.7-alpine


# -- Install Application into container:
RUN set -ex && mkdir /app && apk --update add postgresql-dev gcc python3-dev musl-dev \
   && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . .

# -- Install dependencies:
RUN set -ex && pip install -r requirements.txt