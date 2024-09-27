import asyncio
import uvicorn

from app.backend import app

loop = asyncio.get_event_loop()
application = loop.run_until_complete(app.create_app())

if __name__ == "__main__":
    uvicorn.run(application, host="127.0.0.1", port=8000)
