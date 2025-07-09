from .clientes import get_processo
from apps.datajud_client.adapters.datajud_adapter import DatajudAdapter
from apps.datajud_client.adapters.tjsp_adapter import TJSPAdapter
from apps.datajud_client.adapters.tjrj_adapter import TJRJAdapter

ADAPTERS = {
    "DATAJUD": DatajudAdapter(),
    "TJSP": TJSPAdapter(),
    "TJRJ": TJRJAdapter(),
}

def consultar_por_numero(tribunal: str, numero: str) -> dict:
    adapter = ADAPTERS.get(tribunal)
    if not adapter:
        return {"erro": f"Tribunal '{tribunal}' não suportado."}
    return adapter.consultar_por_numero(numero)

def consultar_por_documento(tribunal: str, documento: str) -> dict:
    adapter = ADAPTERS.get(tribunal)
    if not adapter:
        return {"erro": f"Tribunal '{tribunal}' não suportado."}
    return adapter.consultar_por_documento(documento)

def consultar_processo(numero_processo: str) -> dict:
    """
    Serviço de alto nível para consultar processo no Datajud.
    Aqui você pode adicionar cache, logs, etc.
    """
    return get_processo(numero_processo)
