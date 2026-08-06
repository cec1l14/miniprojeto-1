"""Menu interativo no terminal.

Uso: python cli.py catalogo_final.json
"""
import sys
from catalogo import Catalogo

catalogo = Catalogo(sys.argv[1])

while True:
    print('''
TrilhaSonora
============
1. Listar todos os usuários
2. Ver playlist completa de um usuário
3. Conteúdo na posição N da playlist
4. Interseção de playlists (N usuários)
5. Dados de um conteúdo (rating, duração, gêneros, plataformas, data, execuções)
6. Conteúdos de um gênero
7. Enfileirar conteúdo na fila de reprodução
8. Tocar próximo da fila
9. Ver fila atual
0. Sair
'''
          )
    pedido = int(input("> "))

    if (pedido == 0):
        print("Fim.")
        break
        
    elif (pedido < 1) or (pedido > 9):
        print("Opção inválida.")

    else: 

        if pedido == 1:
            print(f"{len(catalogo.listar_usuarios())} usuários (ordem alfabética)")

            for i in catalogo.listar_usuarios():
                print(i)

        elif pedido == 2:
            nome = input("Nome do usuário: ")
            usuario_id = catalogo.buscar_usuario_por_nome(nome)

            if usuario_id is None:
                print("Usuário não encontrado.")
            else:
                playlist = catalogo.playlist_de(usuario_id)
                for i in range(len(playlist)):
                    playlist_nome = catalogo.descricao_de(playlist[i])
                    print(f"{i+1}. {playlist_nome}")

        elif pedido == 3:
            nome = input("Nome do usuário: ")
            id_us = catalogo.buscar_usuario_por_nome(nome)

            if id_us is None:
                print("Usuário não encontrado.")
            else:
                playlist = catalogo.playlist_de(id_us)
                print(f"Playlist de {nome} tem {len(playlist)} itens (posições de 1 a {len(playlist)}).")

                posicao = int(input("Posição: ")) 

                result = catalogo.conteudo_na_posicao(id_us, (posicao-1))

                print(f"Posição {posicao} de {nome}: {catalogo.descricao_de(result)}")

        elif pedido == 4:
            pass

        elif pedido == 5:
            id_cont = input("ID do conteúdo (ex.: t000000): ")

            print(f"rating: {catalogo.rating_de(id_cont)}")
            print(f"duração: {catalogo.duracao_total_de(id_cont)}")
            print(f"gêneros: {catalogo.generos_de(id_cont)}")
            print(f"plataformas: {catalogo.plataformas_de(id_cont)}")
            print(f"adicionado: {catalogo.data_adicionado_de(id_cont)}")
            print(f"execuções: {catalogo.execucoes_de(id_cont)}")

        elif pedido == 6:
            genero = input("Gênero (ex.: Pop): ")

            conteudo_g = catalogo.conteudos_do_genero(genero)

            for i in conteudo_g:
                print(f"- {i}")
    
        elif pedido == 7:
            id_fila = input("ID do conteúdo para enfileirar (ex.: t000000): ")
            resultado = catalogo.enfileirar(id_fila)

            if resultado:
                print(f"Enfileirado: {catalogo.descricao_de(id_fila)}")

        elif pedido == 8:
            musica = catalogo.proximo()

            if musica is None:
                print("Fila vazia.")
            else:
                print(f"Tocando: {catalogo.descricao_de(musica)}")


        elif pedido == 9:
            fila = catalogo.fila_atual()

            if not fila:
                print("Fila vazia.")
            else:
                for i in fila:
                    print(catalogo.descricao_de(i))