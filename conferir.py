"""Compara respostas.json com gabarito_publico.json.

Uso: python3 conferir.py
"""

import json


def verificar(esperado, obtido):
    if isinstance(esperado, float) and isinstance(obtido, (int, float)):
        return abs(esperado - obtido) < 1e-6

    return esperado == obtido


def main():
    with open("gabarito_publico.json", encoding="utf-8") as f:
        gabarito = json.load(f)

    with open("respostas.json", encoding="utf-8") as f:
        respostas = json.load(f)

    certas = 0
    erradas = []
    ausentes = []

    for chave, esperado in gabarito.items():
        
        if chave not in respostas:
            ausentes.append(chave)
            continue

        obtido = respostas[chave]

        if verificar(esperado, obtido):
            certas += 1
        else:
            erradas.append((chave, esperado, obtido))

    total = len(gabarito)
    print(f"{certas} respostas certas de {total}")

    if ausentes:
        print(f"\n{len(ausentes)} ausentes:")
        for chave in ausentes:
            print(f"  id {chave}")

    if erradas:
        print(f"\n{len(erradas)} erradas:")
        for chave, esperado, obtido in erradas:
            print(f"  id {chave}: esperado={esperado!r}, obtido={obtido!r}")


if __name__ == "__main__":
    main()