from conf.base import *

DEBUG = True

DATABASE_URI = f'sqlite:///{pathlib.Path(ROOT_PATH, "test.db")}'
