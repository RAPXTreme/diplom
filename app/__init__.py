from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/", response_class=RedirectResponse)
def redirect_home():
    return RedirectResponse("/home")
