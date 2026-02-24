from fastapi import APIRouter
from backend.services.etl_service import EtlService

non_kpi_router = APIRouter()

@non_kpi_router.get("/non-kpi/errors")
def get_errors():
    result = EtlService().run()
    return result["errors"]

