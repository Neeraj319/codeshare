from fastapi import FastAPI
from auth.urls import router
from codeshare.db_init import main, close_db_connection
from admin.urls import router as admin_router
import asyncio
from fastapi_pagination import add_pagination
app = FastAPI()
loop = asyncio.get_event_loop()
asyncio.gather(main())
app.include_router(router)
app.include_router(admin_router)


add_pagination(app)


@app.on_event("shutdown")
def shutdown():
    asyncio.gather(close_db_connection())
