FROM python:3.10-alpine as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG USERNAME=www

RUN addgroup www

RUN adduser -g "pcluser" \
    -D \
    -s /bin/bash \
    -u 1001 \
    -G www \
    ${USERNAME} && \
    echo "$USERNAME:1234" | chpasswd


RUN set -ex  && apk update \
    && apk add linux-headers gcc python3-dev musl-dev libffi-dev \
    && apk add postgresql-dev


USER www

WORKDIR /home/www/app/

USER root

COPY --chown=www:www ./stacktrails/requirements.txt ./

RUN  pip install --upgrade pip

RUN pip install -r requirements.txt

COPY --chown=www:www ./docker/app/entrypoint.sh /usr/local/bin/entrypoint.sh


RUN chmod +x  /usr/local/bin/entrypoint.sh

USER www

COPY --chown=www:www ./stacktrails  ./

EXPOSE 8080

ENV port 8080

ENTRYPOINT [ "entrypoint.sh" ]


FROM base as dev

USER root

COPY --chown=www:www ./docker/app/dev.startup.sh /usr/local/bin/

RUN chmod a+x /usr/local/bin/dev.startup.sh

USER www

CMD ["dev.startup.sh"]


FROM base as prefork

USER root

COPY --chown=www:www ./docker/app/prefork.sh /usr/local/bin/

RUN chmod a+x /usr/local/bin/prefork.sh

USER www

# add celery command in run command

FROM base as prod

USER root

COPY --chown=www:www ./docker/app/prod.startup.sh /usr/local/bin/

RUN chmod a+x /usr/local/bin/prod.startup.sh

USER www

RUN  pip3 install uwsgi -I --no-cache-dir


CMD ["prod.startup.sh"]








