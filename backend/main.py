import sys
from pathlib import Path
from api.kpi import kpi_router

sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI
from shared import setup_logging

setup_logging()
app = FastAPI()
app.include_router(kpi_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


