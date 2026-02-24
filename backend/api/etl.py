from fastapi import APIRouter, HTTPException
from backend.services.etl_service import EtlService

etl_router = APIRouter()

@etl_router.post("/etl/run")
def run_etl_endpoint():
    try:
        result = EtlService().run()
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de l'exécution de l'ETL.")

