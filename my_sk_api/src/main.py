from fastapi import FastAPI
from .routers.user import user_router
from .routers.calendar import calendar_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

def setup_application() -> FastAPI:
    """
    Do the required setting up
    """

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = setup_application()
app.include_router(user_router)
app.include_router(calendar_router)
