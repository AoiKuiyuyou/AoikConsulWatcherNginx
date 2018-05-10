[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikConsulWatcherNginx
Watch changes of Consul services and update Nginx config.

Tested woring with:
- Python 3.6.5, 2.7.14

## Table of Contents
[:toc(beg='next', indent=-1)]

## Setup
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikConsulWatcherNginx

cd AoikConsulWatcherNginx

pip install -r aoikconsulwatcher/requirements.txt
```

## Usage
[:tod()]

### Edit config module
Edit AoikConsulWatcher config module [aoikconsulwatcher/conf/config.py](/aoikconsulwatcher/conf/config.py). This config module specifies the Consul
server to connect to, and the handler `handle_service_infos` to be called on changes of Consul services. The handler renders a Jinja2 template [nginx/nginx_sites.conf.template](/nginx/nginx_sites.conf.template) into file
`/etc/nginx/sites-enabled/nginx_sites.conf` and asks Nginx to reload config.

Edit Nginx config template [nginx/nginx_sites.conf.template](/nginx/nginx_sites.conf.template).

### Run program
Run:
```
cd AoikConsulWatcherNginx

export CONSUL_HOST=127.0.0.1
export CONSUL_PORT=8500
export TEMPLATE_FILE_PATH=nginx/nginx_sites.conf.template

python aoikconsulwatcher/src/aoikconsulwatcher/__main__.py --config aoikconsulwatcher/conf/config.py
```

## Docker
The docker image runs an Nginx server and an AoikConsulWatcher process that
updates Nginx config on changes of Consul services.

[:tod()]

### Run image
Run:
```
docker run -it -p 80:80 -p 443:443 \
    -e CONSUL_HOST=127.0.0.1 \
    -e CONSUL_PORT=8500 \
    aoikuiyuyou/aoikconsulwatchernginx
```
Or:
```
cd AoikConsulWatcherNginx

docker-compose -f docker/docker-compose.yml up
```

To use a custom AoikConsulWatcher config module e.g. `/config.py`, run:
```
docker run -it -p 80:80 -p 443:443 \
    -v /config.py:/opt/aoikconsulwatchernginx/aoikconsulwatcher/conf/config.py \
    -e CONSUL_HOST=127.0.0.1 \
    -e CONSUL_PORT=8500 \
    aoikuiyuyou/aoikconsulwatchernginx
```

To use a custom Nginx config template e.g. `/nginx_sites.conf.template`, run:
```
docker run -it -p 80:80 -p 443:443 \
    -v /nginx_sites.conf.template:/opt/aoikconsulwatchernginx/nginx/nginx_sites.conf.template \
    -e CONSUL_HOST=127.0.0.1 \
    -e CONSUL_PORT=8500 \
    aoikuiyuyou/aoikconsulwatchernginx
```

### Build image
Run:
```
cd AoikConsulWatcherNginx

docker build -t aoikuiyuyou/aoikconsulwatchernginx -f docker/Dockerfile .
```
