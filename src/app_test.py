import os

from flask import Flask

from core.db import setup_sqla
from core.routes import setup_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object('conf.test')
    app.debug = True
    setup_routes(app=app, url_paths=app.config['ROUTE_PATHS'])
    return app


app = create_app()
app.app_context().push()
