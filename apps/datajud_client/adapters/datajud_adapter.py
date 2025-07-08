import logging
from .base import BaseAdapter

logger = logging.getLogger(__name__)

class DatajudAdapter(BaseAdapter):
    """
    Adapter do Datajud (CNJ).
    """

    def consultar_por_numero(self, numero_processo: str) -> dict:
        logger.info(f"Datajud - consultando por número {numero_processo}")

        try:
            # Aqui você coloca a chamada real ao seu client (services/clients)
            from apps.datajud_client.clients import get_processo
            raw = get_processo(numero_processo)

            return {
                "fonte": "Datajud",
                "resultado": raw
            }

        except Exception as e:
            logger.error(f"Erro na consulta Datajud: {e}")
            return {"erro": "Falha na consulta Datajud."}

    def consultar_por_documento(self, documento: str) -> dict:
        logger.warning("Consulta por documento não implementada no Datajud")
        return {"erro": "Consulta por documento não suportada no Datajud."}
