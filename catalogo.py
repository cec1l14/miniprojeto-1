"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""
import json
from collections import deque

'''
Sujeiras:
    1. rating ausente
    2. rating como str
    3. dois formatos de data
    4. generos como str
    5. generos como lista aninhada
    6. engajamento com virgula
    7. duracao_seg como null
'''

# Funções para a limpeza

def verificar_rating(rating):
    if rating is None:
        return None
    else:
        return float(rating)

def limpar_data(data_adicionado):
    if data_adicionado is None:
        return None
    elif '/' in data_adicionado:
        dia, mes, ano = data_adicionado.split('/')
        return f'{ano}-{mes}-{dia}'
    else:
        return data_adicionado

def limpar_execucoes(engajamento_execucoes):
    if engajamento_execucoes is None:
        return None
    
    elif isinstance(engajamento_execucoes, str):
        engajamento_execucoes = engajamento_execucoes.replace(',','')

    return int(engajamento_execucoes)


        
def __init__(self, caminho_json: str): 

    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]: ...
    def buscar_usuario_por_nome(self, nome: str) -> str | None: ...
    def playlist_de(self, usuario_id: str) -> list[str] | None: ...
    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None: ...
    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]: ...

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None: ...
    def duracao_total_de(self, conteudo_id: str) -> int | None: ...
    def generos_de(self, conteudo_id: str) -> list[str] | None: ...
    def plataformas_de(self, conteudo_id: str) -> list[str] | None: ...
    def data_adicionado_de(self, conteudo_id: str) -> str | None: ...
    def execucoes_de(self, conteudo_id: str) -> int | None: ...
    def conteudos_do_genero(self, genero: str) -> list[str]: ...

    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool: ...
    def proximo(self) -> str | None: ...
    def fila_atual(self) -> list[str]: ...
