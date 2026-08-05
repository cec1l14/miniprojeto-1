# Mini-Projeto TrilhaSonora

> **Entrega: sexta-feira, 07/08/2026.**
> Link do repositório no formulário de entrega da aula 09:
> **<https://www.otrilha.com/aulas/09>**. Só o link, nada de zip, nada de email.

Vocês vão construir um analisador do catálogo da **TrilhaSonora**, uma
plataforma fictícia de streaming musical. O resultado é um produto de verdade:
uma classe que modela o catálogo, um menu interativo no terminal e um modo
batch que responde 10 mil consultas de uma vez.

---

## Minhas explicações

Inicialmente, como solicitado, coloquei em "catalogo.py" a classe Catálogo e os métodos obrigatórios
de análise. Após isso, resolvi tratar os 7 problemas de limpeza presente no json. Para tal, criei 
algumas funções auxiliares. Logo, defini: 


1. verificar_rating(): essa função faz as duas primeiras limpezas solicitadas, haja vista que verifica se o
rating possui conteúdo **None**. Caso exista outro conteúdo, ele faz a conversão para
o tipo float.
```python
def verificar_rating(rating):
    if rating is None:
        return None
    return float(rating)
```
2. limpar_data(): essa função tem por objetivo escrever a data no padrão americano (ano/mês/dia) e com o traço separador '-'.
```python
def limpar_data(data_adicionado):
    if data_adicionado is None:
        return None
    elif '/' in data_adicionado:
        dia, mes, ano = data_adicionado.split('/')
        return f'{ano}-{mes}-{dia}'
    else:
        return data_adicionado
```
3. limpar_execucoes(): agora faz-se a verificação da variável engajamento_execucoes. Caso ela seja do tipo str, a função
verificará se há vírgula ou não (caso haja, será substituída por 'nada').
```python
def limpar_execucoes(engajamento_execucoes):
    if engajamento_execucoes is None:
        return None
    
    elif isinstance(engajamento_execucoes, str):
        engajamento_execucoes = engajamento_execucoes.replace(',','')

    return int(engajamento_execucoes)
```
4. limpar_generos(): por meio dessa função, duas sujeiras são limpadas simultaneamente. Caso o conteúdo de 'gêneros' seja uma str, havéra a conversão desta para uma lista. Caso a lista esteja aninhada, como proposto, haverá o tratamento de erro por meio de manipulação de pilhas.
```python
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
```
5. limpar_duracao(): garante que se existir, em duracao_seg, um campo vazio, este será substituído por 0, a fim de facilitar a soma da duração final.
```python
def limpar_duracao(duracao_seg):
    if duracao_seg is None:
        return 0
    return int(duracao_seg)
```

Após essa etapa, parti para a análise do **_ _init_ _**. Para tal, como sugerido no enunciado da atividade, criei um dicionário cuja chave é **id** e o valor é o conteúdo armazenado do caminho json (caminho este aberto também no _ _init_ _).
```python
  def __init__(self, caminho_json: str):  
      with open(caminho_json, encoding="utf-8") as f:
          dados = json.load(f)

      self._conteudos = {}
      for i in dados["conteudos"]:
          self._conteudos[i["id"]] = i
```
E, posteriormente, chamei as funções auxiliares nos métodos para dados de conteúdo. Como exemplo, tem-se:
```python
  def rating_de(self, conteudo_id: str) -> float | None: 
    conteudo = self._conteudos.get(conteudo_id)

    if conteudo is None:
      return None

    return verificar_rating(conteudo.get("rating"))
```

A fim de deixar um pouco menos abstrato para meu entendimento, resolvi entrar no modo interativo do python e fazer alguns testes (com auxílio do Claude):
```python
>>> print(c.rating_de("t000002"))
9.2
>>> print(c.rating_de("t000009"))
8.5
>>> print(c.data_adicionado_de("t000002"))
2023-04-08
>>> print(c.data_adicionado_de("t000009"))
2023-07-27
>>> print(c.data_adicionado_de("t999999"))
None
>>> print(c.generos_de("t000009"))
['Smooth Jazz', 'Soul']
```