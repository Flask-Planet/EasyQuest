from os import environ

bind = "0.0.0.0:5000"
workers = 3
wsgi_app = "app:create_app()"

if environ.get("FLASK_ENV") == "development":
    reload = True
    capture_output = True
