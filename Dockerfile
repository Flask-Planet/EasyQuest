FROM easyquest-base:latest

# set workdir
WORKDIR /easyquest

# environment variables
COPY .env .env

# copy files
COPY app app
COPY production_configs/gunicorn.conf.py gunicorn.conf.py
COPY production_configs/supervisord.conf supervisord.conf
COPY production_configs/nginx.config /etc/nginx/http.d/default.conf

# start
ENTRYPOINT ["supervisord", "-c", "supervisord.conf"]