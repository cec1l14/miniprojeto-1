# Mini-Projeto TrilhaSonora

> **Entrega: sexta-feira, 07/08/2026.**
> Link do repositório no formulário de entrega da aula 09:
> **<https://www.otrilha.com/aulas/09>**. Só o link, nada de zip, nada de email.

Vocês vão construir um analisador do catálogo da **TrilhaSonora**, uma
plataforma fictícia de streaming musical. O resultado é um produto de verdade:
uma classe que modela o catálogo, um menu interativo no terminal e um modo
batch que responde 10 mil consultas de uma vez.

---

## Primeiros passos

Inicialmente, como solicitado, coloquei em "catalogo.py" a classe Catálogo e os métodos obrigatórios
de análise. Após isso, resolvi tratar os 7 problemas de limpeza presente no json. Para tal, criei 
algumas funções auxiliares. Logo, defini: 


1. verificar_rating(): essa função faz as duas primeiras limpezas solicitadas, haja vista que verifica se o
rating possui conteúdo **None** (Python converte Null, do json, em None). Caso exista outro conteúdo, ele faz a conversão para
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
