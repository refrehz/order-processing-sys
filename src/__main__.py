import asyncio
from fastapi import FastAPI
from uvicorn import Config, Server

from . import customers
from . import orders
from . import order_items
from . import payment_methods
from . import db


app = FastAPI()


app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(order_items.router)
app.include_router(payment_methods.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Order Processing API!"}


async def run():
    await db.initialize()
    web_server = Server(Config(app=app, host="0.0.0.0", port=8000))
    await web_server.serve()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_soon(lambda: asyncio.create_task(run()))
    loop.run_forever()
