import os
import asyncio
import httpx
from typing import List

API_KEY = os.getenv("DATAJUD_API_KEY", "")
BASE_URL = "https://api-publica.datajud.cnj.jus.br"

TRIBUNAIS_DATAJUD: list[str] = [
    # TRFs
    "trf1", "trf2", "trf3", "trf4", "trf5", "trf6",
    # TJs (principais — adicione outros se precisar)
    "tjsp", "tjrj", "tjmg", "tjba", "tjrs", "tjpr", "tjsc",
    "tjpe", "tjce", "tjpa", "tjgo", "tjma", "tjpb", "tjrn",
    "tjms", "tjmt", "tjro", "tjpi", "tjse", "tjto", "tjam",
    "tjap", "tjac", "tjal", "tjrr", "tjdft", "tjes",
    # Superiores
    "tst", "tse", "stj", "stm",
]

HEADERS = {
    "Authorization": f"ApiKey {API_KEY}",
    "Content-Type": "application/json",
}

QUERY_TEMPLATE = lambda n: {"query": {"match": {"numeroProcesso": n}}}


async def _fetch(client: httpx.AsyncClient, tribunal: str, payload: dict) -> List[dict]:
    url = f"{BASE_URL}/api_publica_{tribunal}/_search"
    try:
        r = await client.post(url, headers=HEADERS, json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()

        hits = (
            data.get("hits", {}).get("hits", [])
            or data.get("resultados", [])
            or []
        )

        normalizados = []
        for hit in hits:
            # Se vier no formato Elasticsearch, use _source
            if "_source" in hit:
                proc = hit["_source"]
            else:
                proc = hit
            proc["fonte_tribunal"] = tribunal
            normalizados.append(proc)
        return normalizados

    except Exception as exc:  # noqa: BLE001
        # log, mas não interrompe
        print(f"[DataJud] erro em {tribunal}: {exc}")
        return []


async def buscar_por_numero(numero_processo: str, tribunais: list[str] | None = None) -> List[dict]:
    """
    Busca simultaneamente em vários tribunais e deduplica pelo número do processo.
    """
    if tribunais is None:
        tribunais = TRIBUNAIS_DATAJUD

    payload = QUERY_TEMPLATE(numero_processo)

    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
    async with httpx.AsyncClient(limits=limits) as client:
        tasks = [_fetch(client, t, payload) for t in tribunais]
        resultados_por_tribunal = await asyncio.gather(*tasks)

    # Achata a lista e deduplica
    vistos, unicos = set(), []
    for lista in resultados_por_tribunal:
        for proc in lista:
            numero = proc.get("numeroProcesso") or proc.get("numero") or proc.get("numero_processo")
            if numero and numero not in vistos:
                vistos.add(numero)
                unicos.append(proc)
    return unicos


# Helper síncrono para ser usado em views ou comandos Django sem async/await
def consultar_processo(numero: str, tribunais: list[str] | None = None) -> List[dict]:
    return asyncio.run(buscar_por_numero(numero, tribunais))
