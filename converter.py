import requests
import json
from datetime import datetime

def obter_cotacao(moeda_origem: str, moeda_destino: str) -> float:
    try:
        url = f"https://economia.awesomeapi.com.br/json/last/{moeda_destino}-{moeda_origem}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        par = f"{moeda_destino}{moeda_origem}"
        return float(data[par]["bid"])
    except Exception as e:
        raise RuntimeError(f"Erro ao obter cotação: {e}")

def salvar_historico(origem: str, destino: str, valor_origem: float, valor_convertido: float):
    entrada = {
        "data": datetime.now().isoformat(),
        "moeda_origem": origem,
        "moeda_destino": destino,
        "valor_origem": valor_origem,
        "valor_convertido": valor_convertido
    }
    with open("historico.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada) + "\n")
