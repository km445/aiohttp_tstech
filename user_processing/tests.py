import os
from time import time

from aiohttp import web
from aiohttp.test_utils import TestClient
from aiohttp.test_utils import TestServer
from aiohttp.test_utils import loop_context
from aiohttp import request
import aiohttp_jinja2
import jinja2
import aiomysql.sa

from settings import DB_CONFIG
from settings import ENGINE_PARAMETERS
from settings import BASE_DIR
from routes import setup_routes
from middlewares import setup_middlewares
from db import init_mysql
from db import close_mysql
from db import users


def create_example_app():
    app = web.Application()
    template_dir = os.path.join(BASE_DIR, "user_processing", "templates")
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(template_dir))
    setup_routes(app)
    setup_middlewares(app)
    app.on_startup.append(init_mysql)
    app.on_cleanup.append(close_mysql)
    return app


async def get_mysql_engine():
    engine = await aiomysql.sa.create_engine(
        db=DB_CONFIG["database"],
        user=DB_CONFIG["username"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        maxsize=ENGINE_PARAMETERS["pool_size"])
    return engine


async def close_mysql_engine(engine):
    engine.close()
    await engine.wait_closed()


with loop_context() as loop:
    app = create_example_app()
    client = TestClient(TestServer(app), loop=loop)
    loop.run_until_complete(client.start_server())

    async def test_index_get_route():
        # Verify successful get request
        resp = await client.get("/")
        assert resp.status == 200
        text = await resp.text()
        assert "Submit user data" in text

    async def test_index_post_route_success():
        # Verify successful post request
        start_time = time()
        user_data = {"age": 1, "name": "Bob", "city": "Oakland"}
        resp = await client.post(
            "/", data=user_data)

        # Assert that there is a delay of 10 seconds
        assert (time() - start_time) >= 10
        assert resp.status == 200
        text = await resp.text()
        assert "Your data has been saved and processed" in text

        # Assert that data is saved in the database
        engine = await get_mysql_engine()
        async with engine.acquire() as conn:
            cursor = await conn.execute(
                users.select().order_by(users.c.id.desc()).limit(1))
            record = await cursor.fetchone()
            assert record.age == user_data["age"]
            assert record.name == user_data["name"]
            assert record.city == user_data["city"]
        await close_mysql_engine(engine)

    async def test_index_post_route_failure():
        # Verify failed post request
        resp = await client.post("/", data={"age": 1, "city": "Oakland"})
        assert resp.status == 200
        text = await resp.text()
        assert "Invalid user data, name is required." in text
        resp = await client.post("/", data={"name": "Bob", "city": "Oakland"})
        text = await resp.text()
        assert "Invalid user data, age is required." in text
        resp = await client.post("/", data={"name": "Bob", "age": 1})
        text = await resp.text()
        assert "Invalid user data, city is required." in text
        # Verify invalid age
        resp = await client.post(
            "/", data={"name": "Bob", "age": "q", "city": "Oakland"})
        text = await resp.text()
        assert "Invalid user age." in text

    loop.run_until_complete(test_index_get_route())
    loop.run_until_complete(test_index_post_route_success())
    loop.run_until_complete(test_index_post_route_failure())
    loop.run_until_complete(client.close())
