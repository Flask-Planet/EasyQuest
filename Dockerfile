FROM python:3.11-alpine

# timezone
ENV TZ=Europe/London

# set workdir
WORKDIR /easyquest

# environment variables
COPY .env .env

# copy files
COPY app app
COPY production_configs/gunicorn.conf.py gunicorn.conf.py
COPY production_configs/supervisord.conf supervisord.conf
COPY requirements/production.txt requirements.txt

# create uploads folder
RUN mkdir /easyquest/instance
RUN mkdir /easyquest/instance/uploads

# install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# start
ENTRYPOINT ["supervisord", "-c", "supervisord.conf"]