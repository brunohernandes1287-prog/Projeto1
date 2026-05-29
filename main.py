import os
import time
import Repositorio as repo
import menu as menus

repo.carregar_json()

def _buscar_e_exibir():
    ativo = menus.buscar_ativo()
    if ativo:
        print(ativo)
    input("\nPressione Enter para voltar...")

OPCOES = {
    1: menus.cadastrar_ativo,
    2: _buscar_e_exibir,
    3: menus.atualizar_ativo,
    4: menus.remover_ativo,
    5: menus.listar_ativos,
    6: menus.adicionar_vulnerabilidade,
    7: menus.ver_vulnerabilidades,
    8: menus.consertar_vulnerabilidade,
}

while True:
    
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 35)
    print("   GERENCIADOR DE ATIVOS")
    print("=" * 35)
    print("""
Ativos---------------------------------
1 - Cadastrar ativo
2 - Buscar ativo
3 - Atualizar ativo
4 - Remover ativo
5 - Listar ativos
Vulnerabilidades-----------------------
6 - Adicionar vulnerabilidade
7 - Ver vulnerabilidades
8 - Consertar vulnerabilidade
----------------------------------------
0 - Sair
""")
    try:
        opcao = int(input("Escolha uma opcao: "))
    except ValueError:
        print("\n⚠️ Digite um número válido.")
        time.sleep(2)
        continue

    if opcao == 0:
        print("\nSaindo...")
        break

    acao = OPCOES.get(opcao)
    if acao:
        acao()
    else:
        print("\n⚠️ Opção inválida.")
        time.sleep(2)