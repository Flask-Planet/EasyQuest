from flask import current_app as app


@app.get("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")
