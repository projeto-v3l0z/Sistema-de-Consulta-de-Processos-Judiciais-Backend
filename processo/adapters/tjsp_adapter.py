# Adaptador do tjsp
import requests
from datetime import datetime
from processo.adapters.base_adapter import BaseAdapter
from processo.dtos import ProcessoDTO

class TjspAdapter(BaseAdapter):
    """
    Adaptador para o Tribunal de Justiça de São Paulo (TJSP).
    Realiza requisições via SAJ-ESAJ e converte para o formato padrão.
    """
    BASE_URL = "https://esaj.tjsp.jus.br/cposg5/search.do"

    def fetch_raw(self, numero_processo: str) -> dict:
        """
        Busca os dados brutos do processo no TJSP.
        """
        params = {
            'conversationId': '',
            'paginaConsulta': '1',
            'localPesquisa.cdLocal': '28', 
            'cbPesquisa': 'NUMPROC',
            'dadosConsulta.nuProcesso': numero_processo
        }
        resp = requests.get(self.BASE_URL, params=params)
        resp.raise_for_status()
        # Caso a resposta seja HTML, implemente parsing com BeautifulSoup
        return resp.json()

    def to_standard_format(self, raw_data: dict) -> ProcessoDTO:
        """
        Converte o JSON do TJSP para ProcessoDTO.
        """
        proc = raw_data.get('processo', {})
        num = proc.get('numeroProcesso', '') or proc.get('numProcesso', '')
        # Data originalmente em 'DD/MM/YYYY'
        data_str = proc.get('dataDistribuicao', '')
        data_iso = ''
        if data_str:
            try:
                data_iso = datetime.strptime(data_str, '%d/%m/%Y').date().isoformat()
            except ValueError:
                data_iso = data_str

        return ProcessoDTO(
            numero_processo=num,
            tribunal='TJSP',
            classe_processual=proc.get('classeProcessual', '').strip(),
            assunto=proc.get('assunto', '').strip(),
            data_distribuicao=data_iso,
            orgao_julgador=proc.get('vara', '').strip(),
            situacao_atual=proc.get('situacaoProcesso', '').strip(),
        )
    
    def consultar_por_documento(self, documento: str) -> list[ProcessoDTO]:
        resp = requests.get(f"{self.BASE_URL}por-documento/{documento}")
        resp.raise_for_status()
        raw_list = resp.json().get('processos', [])
        return [ self.to_standard_format(raw) for raw in raw_list ]