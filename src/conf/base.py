import pathlib


BASE_PATH = pathlib.Path(__file__)
ROOT_PATH = BASE_PATH.parents[2]

DEBUG = True

ROUTE_PATHS = [
    'apps.servers.routes',
]

MODEL_PATHS = [
    'apps.servers.models',
]

DATABASE_URI = f'sqlite:///{pathlib.Path(ROOT_PATH, "sqlite.db")}'

