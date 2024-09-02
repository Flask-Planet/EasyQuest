FROM easyquest-base:latest

# set workdir
WORKDIR /easyquest

# environment variables
COPY .production_env .env

# copy files
COPY app app
COPY configs/gunicorn.conf.py gunicorn.conf.py
COPY configs/supervisord.conf supervisord.conf
COPY configs/nginx.config /etc/nginx/http.d/default.conf

# start
ENTRYPOINT ["supervisord", "-c", "supervisord.conf"]