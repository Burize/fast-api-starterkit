from fastapi import FastAPI
from core import settings
from core.initialize_app import init_app

app = FastAPI(
    title='starter',
    docs_url=f"{settings.API_PREFIX}/docs",
)


init_app(app)
