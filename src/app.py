import os

from flask import Flask

from core.db import setup_sqla
from core.routes import setup_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_SETTINGS', 'conf.dev'))
    app.debug = app.config['DEBUG']
    setup_sqla(app, app.config['MODEL_PATHS'])
    setup_routes(app=app, url_paths=app.config['ROUTE_PATHS'])
    return app


def main():
    app = create_app()
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
