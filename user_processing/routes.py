import os

from aiohttp import web

from views import UserHandler
from settings import BASE_DIR


def setup_routes(app):
    """Function to set up application routes."""

    # Set up static routes
    app.router.add_static("/static/",
                          path=os.path.join(BASE_DIR, "static"),
                          name="static")

    # Set up custom routes
    user_handler = UserHandler()
    app.add_routes(
        [web.get("/", user_handler.index),
         web.post("/", user_handler.process_user_data)])
