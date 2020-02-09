import time

from aiohttp import web
from aiohttp_jinja2 import render_template

import db
from utils import Logger


class UserHandler(object):
    """Handler class for user processing."""

    def __init__(self):
        self.required_data = ["name", "age", "city"]

    async def index(self, request):
        """Function which renders a form for user to fill."""

        context = {}
        return render_template("user_processing/user_processing.html",
                               request, context)

    async def process_user_data(self, request):
        """Function which processes user data."""

        # Get user data from request
        user_data = await request.post()

        # Verify user data
        for data_item in self.required_data:
            if user_data.get(data_item) in [None, ""]:
                context = {
                    "message":
                    "Invalid user data, %s is required." % data_item}
                return render_template("user_processing/user_processing.html",
                                       request, context)
        try:
            int(user_data.get("age", ""))
        except ValueError:
            context = {"message": "Invalid user age."}
            return render_template("user_processing/user_processing.html",
                                   request, context)

        # Commit user data to the database
        async with request.app["db"].acquire() as conn:
            await conn.execute(db.users.insert().values(**user_data))
            await conn.execute("commit")

        # Sleep for 10 seconds
        time.sleep(10)

        # Render form with success message
        context = {"message":
                   "Your data has been saved and processed, thank you!"}
        return render_template("user_processing/user_processing.html",
                               request, context)
