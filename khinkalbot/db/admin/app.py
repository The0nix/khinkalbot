import os

from flask import Flask, redirect, url_for
import flask_admin
from flask_admin.contrib.peewee import ModelView
from flask_basicauth import BasicAuth

from khinkalbot.db.models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["ADMIN_SECRET_KEY"]

app.config['BASIC_AUTH_USERNAME'] = os.environ["ADMIN_USERNAME"]
app.config['BASIC_AUTH_PASSWORD'] = os.environ["ADMIN_PASSWORD"]
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


@app.route('/')
def index():
    return redirect("/admin")


def start():
    import logging
    logging.getLogger()

    admin = flask_admin.Admin(app, name='Example: Peewee')

    admin.add_view(ModelView(User))

    app.run(debug=False, host="0.0.0.0", port=os.environ["ADMIN_PORT"])
