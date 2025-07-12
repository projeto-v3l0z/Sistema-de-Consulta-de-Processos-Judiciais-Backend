import requests
from django.conf import settings
def buscar_processo_datajud(numero_processo):
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_trf1/"

    headers = {
        "Authorization": f"Bearer {settings.DATAJUD_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "numeroProcesso": numero_processo
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()

            return {
                "fonte": "Datajud",
                "numero": data.get("numero", numero_processo),
                "status": data.get("status", "Desconhecido"),
                "classe": data.get("classe", "Desconhecida")
            }

        elif response.status_code == 404:
            return None  # Processo não encontrado

        else:
            print(f"Erro DataJud: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Erro na comunicação com DataJud: {e}")
        return None
