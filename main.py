from fastapi import FastAPI
import core.settings as settings
from core.initialize_app import init_app

app = FastAPI(
    title='starter', docs_url=f"{settings.API_PREFIX}/docs"
)


init_app(app)
