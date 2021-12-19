from fastapi import FastAPI, APIRouter
from home.url import router
from db_init import main, close_db_connection
import asyncio

app = FastAPI()
loop = asyncio.get_event_loop()
asyncio.gather(main())
app.include_router(router)


@app.on_event("shutdown")
def shutdown():
    asyncio.gather(close_db_connection())
