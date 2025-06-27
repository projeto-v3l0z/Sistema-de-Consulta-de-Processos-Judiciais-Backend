# serviços para chegar nas APIs de fora
from processo.adapters.datajud_adapter import DatajudAdapter
from processo.adapters.tjsp_adapter import TjspAdapter
from processo.adapters.trj_adapter import TrjAdapter

ADAPTERS = {
    "datajud": DatajudAdapter(),
    "tjsp":   TjspAdapter(),
    "trj":    TrjAdapter(),
}

def get_processo(numero_processo: str, fonte: str):
    adapter = ADAPTERS.get(fonte)
    if not adapter:
        raise ValueError(f"Fonte inválida: {fonte}")

    raw = adapter.fetch_raw(numero_processo)
    dto = adapter.to_standard_format(raw)
    return dto
