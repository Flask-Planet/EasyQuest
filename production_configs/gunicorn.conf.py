from os import environ

bind = "127.0.0.1:5000"
workers = 3
wsgi_app = "app:create_app()"

if environ.get("FLASK_ENV") == "development":
    reload = True
    capture_output = True
