from flask import Flask


def create_app():
    new_app = Flask(__name__)
    new_app.debug = True

    return new_app

app = create_app()  # pragma: no cover
