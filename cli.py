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

        if pedido == 2:
            nome = input("Nome do usuário: ")
            usuario_id = catalogo.buscar_usuario_por_nome(nome)

            playlist = catalogo.playlist_de(usuario_id)
            for i in range(len(playlist)):
                print(f"{i}. {playlist[i]}")

