from fastapi import FastAPI
from routes import router
from uvicorn import run

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    run('main:app', reload=True)