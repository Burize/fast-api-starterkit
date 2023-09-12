from fastapi import Depends
from fastapi import FastAPI
from core import settings
from core.dependencies import prolong_session
from core.initialize_app import init_app

app = FastAPI(
    title='starter',
    docs_url=f"{settings.API_PREFIX}/docs",
    dependencies=[Depends(prolong_session)],
)


init_app(app)
