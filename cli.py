"""Menu interativo no terminal.

Uso: python cli.py catalogo_final.json
"""
import sys
from catalogo import Catalogo
from collections import deque

historico = deque(maxlen = 10)

# função para opção 5

def conversao(segundos):
    min = segundos//60
    resto_seg = segundos % 60

    return f"{min}m{resto_seg}s"

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
10. Ver histórico
0. Sair
'''
          )
    pedido = (input("> "))
    if not pedido.isdigit():
        print("Opção inválida.")
        continue

    pedido = int(pedido)

    if (pedido == 0):
        print("Fim.")
        break
        
    elif (pedido < 1) or (pedido > 10):
        print("Opção inválida.")

    else: 

        if pedido == 1:
            print(f"{len(catalogo.listar_usuarios())} usuários (ordem alfabética)")

            for i in catalogo.listar_usuarios():
                print(i)

            historico.append("Opção 1: listar todos os usuários")

        elif pedido == 2:
            nome = input("Nome do usuário: ")
            usuario_id = catalogo.buscar_usuario_por_nome(nome)

            if usuario_id is None:
                print("Usuário não encontrado.")
            else:
                playlist = catalogo.playlist_de(usuario_id)
                print(f"Playlist de {nome} ({len(playlist)} itens): ")

                for i in range(len(playlist)):
                    playlist_nome = catalogo.descricao_de(playlist[i])
                    print(f"{i+1}. {playlist_nome}")

            historico.append(f"Opção 2: playlist de {nome}")

        elif pedido == 3:
            nome = input("Nome do usuário: ")
            id_us = catalogo.buscar_usuario_por_nome(nome)

            if id_us is None:
                print("Usuário não encontrado.")
            else:
                playlist = catalogo.playlist_de(id_us)
                print(f"Playlist de {nome} tem {len(playlist)} itens (posições de 1 a {len(playlist)}).")

                posicao = input("Posição: ")

                if (not posicao.isdigit()) or (int(posicao) < 1) or (int(posicao) > len(playlist)):
                    print("Posição inválida.")

                else:
                    posicao = int(posicao)
                    result = catalogo.conteudo_na_posicao(id_us, (posicao-1))

                    print(f"Posição {posicao} de {nome}: {catalogo.descricao_de(result)}")

                historico.append(f"Opção 3: conteúdo na posição {posicao} da playlist")

        elif pedido == 4:
            nomes = input("Nome dos usuários separados por vírgula (ex.: Nicholas, Uchoa): ").split(",")
            nomes = [nome.strip() for nome in nomes]

            if (len(nomes) == 1):
                print("Informe pelo menos 2 usuários.")
                continue

            usuario_ids = []
            for i in nomes:
                usuarios = catalogo.buscar_usuario_por_nome(i)

                if usuarios is None:
                    print(f"Usuário(s) não encontrado(s).")
                    usuario_ids = None
                    break

                usuario_ids.append(usuarios)

            if usuario_ids is not None:
                intersecao = catalogo.intersecao_playlists(usuario_ids)

                if not intersecao:
                    print("Não foram encontradas interseções.")
                else:
                    print(f"Interseção ({len(intersecao)} conteúdos): ")
                    for i in intersecao:
                        print(f"- {catalogo.descricao_de(i)}")

            historico.append(f"Opção 4: interseção de playlists")
                
                
        elif pedido == 5:
            id_cont = input("ID do conteúdo (ex.: t000000): ")

            if catalogo.descricao_de(id_cont) is None:
                print("Conteúdo não encontrado.")

            else:  
                print(catalogo.descricao_de(id_cont))
                print(f"rating: {catalogo.rating_de(id_cont)}")
                print(f"duração: {conversao(catalogo.duracao_total_de(id_cont))}")
                print(f"gêneros: {', '.join(catalogo.generos_de(id_cont))}")
                print(f"plataformas: {', '.join(catalogo.plataformas_de(id_cont))}")
                print(f"adicionado: {catalogo.data_adicionado_de(id_cont)}")

                if catalogo.tipo_de(id_cont) == "musica":
                    print(f"execuções: {catalogo.execucoes_de(id_cont)}")

            historico.append(f"Opção 5: dados de um conteúdo")
        

        elif pedido == 6:
            genero = input("Gênero (ex.: Pop): ")

            conteudo_g = catalogo.conteudos_do_genero(genero)

            if not conteudo_g:
                print("Nenhum conteúdo nesse gênero.")

            for i in conteudo_g:
                print(f"- {catalogo.descricao_de(i)}")

            historico.append(f"Opção 6: conteúdo de um gênero")
            
    
        elif pedido == 7:
            id_fila = input("ID do conteúdo para enfileirar (ex.: t000000): ")
            resultado = catalogo.enfileirar(id_fila)

            if resultado:
                print(f"Enfileirado: {catalogo.descricao_de(id_fila)} (fila com {len(catalogo.fila_atual())} itens)")
            else:
                print(f"Id {id_fila} não encontrado — nada foi enfileirado.")

            historico.append(f"Opção 7: enfileirar conteúdo da fila de reprodução")
            

        elif pedido == 8:
            musica = catalogo.proximo()

            if musica is None:
                print("Fila vazia.")
            else:
                print(f"Tocando: {catalogo.descricao_de(musica)}")
                print(f"Restam {len(catalogo.fila_atual())} itens na fila.")

            historico.append(f"Opção 8: tocar próximo da fila")
            
        elif pedido == 9:
            fila = catalogo.fila_atual()

            if not fila:
                print("Fila vazia.")
            else:
                for i in range(len(fila)):
                    print(f"{i+1}. {catalogo.descricao_de(fila[i])}")

            historico.append(f"Opção 9: ver fila atual")

        elif pedido == 10:
            if not historico:
                print("Histórico vazio.")

            else:
                for i in historico:
                    print(f"- {i}")