import uvicorn
from fastapi import FastAPI
from config import setup_logging

setup_logging()
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
