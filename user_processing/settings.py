import os
import logging
import pathlib
from datetime import date

BASE_DIR = pathlib.Path(__file__).parent.parent

DB_CONFIG = {"drivername": "mysql+pymysql",
             "username": "tstech",
             "password": "tstech",
             "host": "localhost",
             "port": 3306,
             "database": "tstech"}

ENGINE_PARAMETERS = {"pool_size": 20,
                     "max_overflow": 0,
                     "pool_pre_ping": True,
                     "pool_recycle": 3600}

# Save logs to ~/logs/tstech
DIRS = {
    "LOG_TO": os.path.join(os.path.expanduser("~"), "logs/tstech")
}

LOGGER = {
    "level": logging.DEBUG,
    "file": "log_{date:%Y-%m-%d}.log".format(date=date.today()),
    "formatter": logging.Formatter("%(asctime)s [%(thread)d:%(threadName)s] "
                                   "[%(levelname)s] - %(name)s:%(message)s"),
    "sqlalch_file": "sqlalch_log_{date:%Y-%m-%d}.log".format(date=date.today())
}
