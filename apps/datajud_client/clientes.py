import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DATAJUD_API_KEY")

BASE_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/"

HEADERS = {
    "Authorization": f"APIKey {API_KEY}",
    "Content-Type": "application/json"
}

client = httpx.Client(
    base_url=BASE_URL,
    headers=HEADERS,
    timeout=10.0
)


def get_processo(numero_processo: str) -> dict:
    """
    Consulta um processo pelo número no Datajud TJSP.
    """
    payload = {
        "query": {
            "match": {
                "numeroProcesso": numero_processo
            }
        }
    }
    response = client.post("/_search", json=payload)
    response.raise_for_status()
    return response.json()
