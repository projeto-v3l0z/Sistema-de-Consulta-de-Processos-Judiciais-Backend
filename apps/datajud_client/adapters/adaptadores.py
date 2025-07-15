from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class Processo:
    id: str
    numero: str
    tribunal: str
    classe: str
    assuntos: List[str]
    movimentos: List[Dict[str, Any]]
    data_ajuizamento: str

class DataJudAdapter:
    @staticmethod
    def to_processo(api_data: Dict[str, Any]) -> Processo:
        source = api_data.get('_source', {})
        return Processo(
            id=api_data.get('_id', ''),
            numero=source.get('numeroProcesso', ''),
            tribunal=source.get('tribunal', ''),
            classe=source.get('classe', {}).get('nome', ''),
            assuntos=[assunto['nome'] for assunto in source.get('assuntos', [])],
            movimentos=source.get('movimentos', []),
            data_ajuizamento=source.get('dataAjuizamento', '')
        )

    @staticmethod
    def build_numero_processo_query(numero: str) -> Dict[str, Any]:
        return {
            "query": {
                "term": {
                    "numeroProcesso.keyword": ''.join(filter(str.isdigit, numero))
                }
            }
        }

    @staticmethod
    def build_text_search_query(text: str, fields: List[str] = None) -> Dict[str, Any]:
        if fields is None:
            fields = [
                "assuntos.nome",
                "movimentos.nome",
                "classe.nome",
                "orgaoJulgador.nome"
            ]
        return {
            "query": {
                "multi_match": {
                    "query": text,
                    "fields": fields,
                    "fuzziness": "AUTO"
                }
            }
        }