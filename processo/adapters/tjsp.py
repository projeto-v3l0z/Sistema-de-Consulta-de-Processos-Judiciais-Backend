def buscar_processo_tjsp(numero_processo):
    # implementar a lógica da API de busca no TJSP 
    if numero_processo == "1234567-89.2023.8.26.0100":
        return {
            "fonte": "TJSP",
            "numero": numero_processo,
            "status": "Encerrado",
            "classe": "Recurso Ordinário"
        }
