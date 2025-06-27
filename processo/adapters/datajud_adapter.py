# Adaptador do datajud
import requests
from processo.adapters.base_adapter import BaseAdapter
from processo.dtos import ProcessoDTO

class DatajudAdapter(BaseAdapter):
    BASE_URL = "https://api.datajud.gov.br/processos/"

    def fetch_raw(self, numero_processo: str) -> dict:
        resp = requests.get(f"{self.BASE_URL}{numero_processo}")
        resp.raise_for_status()
        return resp.json()

    def to_standard_format(self, raw_data: dict) -> ProcessoDTO:
        
        return ProcessoDTO(
            numero_processo=raw_data.get("num", ""),
            tribunal=raw_data.get("tribunal", ""),
            classe_processual=raw_data.get("classe", ""),
            assunto=raw_data.get("assunto", ""),
            data_distribuicao=raw_data.get("data_distribuicao", ""),
            orgao_julgador=raw_data.get("orgao", ""),
            situacao_atual=raw_data.get("situacao", ""),
        )
