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

def limpar_generos(generos):    
    if isinstance(generos, str):
        generos = [generos]

    generos_pilha = []
    pilha = list(generos)

    while pilha:
        elemento = pilha.pop()

        if isinstance(elemento, list):
            pilha.extend(elemento)

        elif isinstance(elemento, str) and elemento not in generos_pilha:
            generos_pilha.append(elemento)

    generos_pilha = sorted(generos_pilha)
    return generos_pilha

def limpar_duracao(duracao_seg):
    if duracao_seg is None:
        return 0
    return int(duracao_seg)

class Catalogo:
    def __init__(self, caminho_json: str):  
        with open(caminho_json, encoding="utf-8") as t:
            dados = json.load(t)

        # criação do deque

        self._fila = deque()

        self._conteudos = {}
        for i in dados["conteudos"]:
            self._conteudos[i["id"]] = i

        self._id_nome = {}
        for i in dados["usuarios"]:
            self._id_nome[i["nome"].lower()] = i["id"] 

        self._usuarios = {}
        for i in dados["usuarios"]:
            self._usuarios[i["id"]] = i

        
    # --- usuários e playlists ---
    

    def listar_usuarios(self) -> list[str]: 
        nomes = []
        for i in self._usuarios.values():
            nomes.append(i["nome"])

        return sorted(nomes)

    
    def buscar_usuario_por_nome(self, nome: str) -> str | None: 
        return self._id_nome.get(nome.lower())


    def playlist_de(self, usuario_id: str) -> list[str] | None: 
        usuario = self._usuarios.get(usuario_id)

        if usuario is None:
            return None

        return usuario["playlist"]


    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None: 
        conteudo_playlist = self.playlist_de(usuario_id)

        if (conteudo_playlist is None) or (posicao < 0) or (posicao >= len(conteudo_playlist)):
            return None

        return conteudo_playlist[posicao]


    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]: 
        playlists = []

        for i in usuario_ids:
            playlist = self.playlist_de(i)

            if playlist is None:
                return []

            playlists.append(set(playlist))

        intersecao = playlists[0]

        for i in playlists[1:]:
            intersecao = intersecao.intersection(i)

        return sorted(intersecao)
        

    # --- dados de um conteúdo ---


    def rating_de(self, conteudo_id: str) -> float | None: 
         conteudo = self._conteudos.get(conteudo_id)

         if conteudo is None:
             return None

         return verificar_rating(conteudo.get("rating"))
    

    def duracao_total_de(self, conteudo_id: str) -> int | None: 
        conteudo = self._conteudos.get(conteudo_id)

        if conteudo is None:
            return None

        if conteudo["tipo"] == "musica":
            return conteudo["duracao_seg"]

        soma_seg = 0

        for i in conteudo["faixas"]:
            soma_seg += limpar_duracao(i["duracao_seg"])

        return soma_seg
        


    def generos_de(self, conteudo_id: str) -> list[str] | None: 
        conteudo = self._conteudos.get(conteudo_id)

        if conteudo is None:
            return None

        return limpar_generos(conteudo.get("generos"))
        


    def plataformas_de(self, conteudo_id: str) -> list[str] | None: 
        conteudo = self._conteudos.get(conteudo_id)

        if conteudo is None:
            return None

        return sorted(conteudo.get("plataformas", [])) # agora ta certo
           


    def data_adicionado_de(self, conteudo_id: str) -> str | None: 
        conteudo = self._conteudos.get(conteudo_id)

        if conteudo is None:
            return None

        return limpar_data(conteudo.get("data_adicionado"))


    def execucoes_de(self, conteudo_id: str) -> int | None: 
        conteudo = self._conteudos.get(conteudo_id)

        if conteudo is None:
            return None

        engajamento = conteudo.get("engajamento", {})

        return limpar_execucoes(engajamento.get("execucoes"))


    def conteudos_do_genero(self, genero: str) -> list[str]: 
        resultado = []

        for i in self._conteudos:
            if genero in self.generos_de(i): # fazendo uso do método anterior
                resultado.append(i)

        return resultado


    # --- fila de reprodução ---


    def enfileirar(self, conteudo_id: str) -> bool: 
        if conteudo_id not in self._conteudos:
            return False

        self._fila.append(conteudo_id)

        return True

    
    def proximo(self) -> str | None: 
        if not self._fila:
            return None

        return self._fila.popleft() 

        
    def fila_atual(self) -> list[str]: 
        return list(self._fila)


    # metodos para o cli 

    def descricao_de(self, conteudo_id: str) -> str | None:
        conteudo = self._conteudos.get(conteudo_id)

        if conteudo is None:
            return None

        return f"{conteudo['titulo']} - {conteudo['artista']} ({conteudo['tipo']})"

    def tipo_de(self, conteudo_id: str) -> str | None: 
        conteudo = self._conteudos.get(conteudo_id)

        if conteudo is None:
            return None

        return conteudo["tipo"]

    