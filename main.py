from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.responses import JSONResponse
from schemas.auth import SuccessMsg, CsrfSettings
from routers import auth, users, tags, schedules
from logging import getLogger, StreamHandler, DEBUG
import sys


logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)
logger.addHandler(handler)
logger.setLevel(DEBUG)


app = FastAPI(
    title="schedule API",
    description="学習用",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tags.router)
app.include_router(schedules.router)

# origins = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/hello", response_model=SuccessMsg)
async def hello():
    print()
    return {"message": "hello world"}
