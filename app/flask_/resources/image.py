from io import BytesIO

from flask import current_app as app
from flask import send_file

img = (
    "4749463837618002800277000021ff0b4e45545343415045322e30030100000021f904090a0000002"
    "..."
    "6dd7958dd89fadd8a19d9c251701003b"
)


@app.get("/image")
def image():
    return send_file(BytesIO(bytes.fromhex(img)), mimetype='image/gif')
