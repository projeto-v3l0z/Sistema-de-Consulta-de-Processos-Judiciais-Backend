from .adapters import datajud, tjsp, tjrj

def buscar_processo_com_fallback(numero_processo):
    fontes = [
        datajud.buscar_processo_datajud,
        tjsp.buscar_processo_tjsp,
        tjrj.buscar_processo_tjrj
    ]

    for fonte in fontes:
        resultado = fonte(numero_processo)
        if resultado:
            return resultado
    return None