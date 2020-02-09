import logging
import traceback

from aiohttp import web
from aiohttp_jinja2 import render_template


async def handle_400(request):
    return render_template("errors/400.html", request, {})


async def handle_403(request):
    return render_template("errors/403.html", request, {})


async def handle_404(request):
    return render_template("errors/404.html", request, {})


async def handle_500(request):
    return render_template("errors/500.html", request, {})


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):
        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override:
                return await override(request)
            return response

        except web.HTTPException as ex:
            logging.error(traceback.format_exc())
            override = overrides.get(ex.status)
            if override:
                return await override(request)
            raise

        except Exception as ex:
            logging.error(traceback.format_exc())
            return await handle_500(request)

    return error_middleware


def setup_middlewares(app):
    overrides = {400: handle_400,
                 403: handle_403,
                 404: handle_404,
                 500: handle_500}
    error_middleware = create_error_middleware(overrides)
    app.middlewares.append(error_middleware)
