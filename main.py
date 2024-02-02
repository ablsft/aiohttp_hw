from aiohttp import web

from db import Session, engine
from models import Base
from views import AdvertisementView, UserView, LoginView


app = web.Application()


async def orm_context(app: web.Application):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        return await handler(request)


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


app.add_routes([
    web.get('/advertisements/{advertisement_id:\d+}/', AdvertisementView),
    web.patch('/advertisements/{advertisement_id:\d+}/', AdvertisementView),
    web.delete('/advertisements/{advertisement_id:\d+}/', AdvertisementView),

    web.get('/advertisements/', AdvertisementView),
    web.post('/advertisements/', AdvertisementView),

    web.get('/users/', UserView),
    web.post('/users/', UserView),
    web.patch('/users/', UserView),
    web.delete('/users/', UserView),

    web.post('/login/', LoginView),
])


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8000)
