import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import streamlit as st


def _base_url() -> str:
    return os.getenv("HEALTHAI_API_URL", "http://localhost:8000").rstrip("/")


@st.cache_data(ttl=60)
def get_json(path: str) -> dict[str, Any]:
    url = f"{_base_url()}/{path.lstrip('/')}"
    req = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as ex:
        if ex.code == 404:
            user_error = "Endpoint indisponible sur le backend."
        else:
            user_error = "Le backend a retourne une erreur."
        return {"success": False, "error": user_error, "debug_error": f"HTTP {ex.code} on {url}"}
    except URLError as ex:
        return {
            "success": False,
            "error": "Service API indisponible. Verifie que le backend tourne et que HEALTHAI_API_URL est correct.",
            "debug_error": f"Network error on {url}: {ex.reason}",
        }
    except Exception as ex:
        return {"success": False, "error": "Erreur inattendue pendant l'appel API.", "debug_error": f"Unexpected error on {url}: {ex}"}


def clear_api_cache() -> None:
    get_json.clear()
