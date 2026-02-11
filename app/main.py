from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

import model
from controller import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    model.init_db()
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )