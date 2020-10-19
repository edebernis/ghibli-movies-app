FROM python:3.9-alpine3.12

COPY . /app

RUN apk --no-cache add --virtual build-dependencies \
                                 gcc \
                                 musl-dev \
                                 linux-headers \
                                 pcre-dev \
    && apk --no-cache add pcre \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk del build-dependencies

RUN addgroup -g 1000 -S app_user && \
    adduser -u 1000 -S app_user -G app_user

EXPOSE 8000

CMD /usr/local/bin/uwsgi --ini /app/uwsgi.ini --need-app