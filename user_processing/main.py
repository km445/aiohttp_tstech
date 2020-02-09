import os
import logging

from aiohttp import web
import aiohttp_jinja2
import jinja2

from settings import BASE_DIR
from settings import DIRS
from settings import LOGGER
from routes import setup_routes
from middlewares import setup_middlewares
from db import init_mysql
from db import close_mysql


# Create logs folder
if not os.path.exists(DIRS["LOG_TO"]):
    os.makedirs(DIRS["LOG_TO"])

# Get WSGI application and set up logging
app = web.Application()
logging.basicConfig(level=LOGGER["level"],
                    filename=os.path.join(DIRS["LOG_TO"], LOGGER["file"]))

# Set up application templates
template_dir = os.path.join(BASE_DIR, "user_processing", "templates")
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(template_dir))

# Set up application routes
setup_routes(app)

# Set up application error handlers
setup_middlewares(app)

# Initialize aiomysql database engine on application startup
app.on_startup.append(init_mysql)

# Close all acquired database connections on application tear down
app.on_cleanup.append(close_mysql)

web.run_app(app)
