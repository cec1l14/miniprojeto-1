"""Modo batch: lê consultas.json, responde todas em ordem, grava respostas.json.

Uso: python3 main.py consultas.json respostas.json
"""
import json
import sys
from catalogo import Catalogo


def main():
    caminho_consultas = sys.argv[1]
    caminho_respostas = sys.argv[2]

    catalogo = Catalogo("catalogo_final.json")

    with open(caminho_consultas, encoding="utf-8") as f:
        dados = json.load(f)

    respostas = {}
    for consulta in dados["consultas"]:
        metodo = getattr(catalogo, consulta["tipo"])
        resultado = metodo(**consulta["parametros"])
        respostas[str(consulta["id"])] = resultado

    with open(caminho_respostas, "w", encoding="utf-8") as f:
        json.dump(respostas, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()