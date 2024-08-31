from flask import current_app as app


@app.get("/robots.txt")
def robots():
    return app.flask_.send_static_file("robots.txt")
