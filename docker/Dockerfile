#
FROM python:3.6.5-slim

MAINTAINER Aoi.Kuiyuyou <aoi.kuiyuyou@gmail.com>

RUN apt-get update && apt-get install -y --no-install-recommends nginx

COPY ./aoikconsulwatcher /opt/aoikconsulwatchernginx/aoikconsulwatcher

RUN pip install -r \
    /opt/aoikconsulwatchernginx/aoikconsulwatcher/requirements.txt

COPY ./nginx /opt/aoikconsulwatchernginx/nginx

RUN mkdir -pv /etc/nginx/conf.d && \
    mkdir -pv /etc/nginx/sites-enabled && \
    rm -rf /etc/nginx/conf.d/* && \
    rm -rf /etc/nginx/sites-enabled/*

RUN mv -fT /opt/aoikconsulwatchernginx/nginx/nginx.conf /etc/nginx/nginx.conf

COPY ./dumb-init/1.2.1/bin/dumb-init_1.2.1_amd64 /sbin/dumb-init

COPY ./runit/2.1.2/bin/runsv /sbin/runsv
COPY ./runit/2.1.2/bin/runsvdir /sbin/runsvdir
COPY ./runit/runsvdir /etc/runsvdir

RUN chmod 755 /sbin/dumb-init && \
    chmod 755 /sbin/runsv && \
    chmod 755 /sbin/runsvdir && \
    chmod 755 /etc/runsvdir/aoikconsulwatcher/run && \
    chmod 755 /etc/runsvdir/nginx/run

RUN apt-get clean

RUN rm -rf /var/cache/apt/* /var/lib/apt/lists/* && \
    rm -rf /root/.cache && \
    rm -rf /tmp/*

WORKDIR /

EXPOSE 80 443

CMD ["/sbin/dumb-init", "/sbin/runsvdir", "/etc/runsvdir"]
