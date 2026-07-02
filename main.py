import os
import time
import Repositorio as repo
import menu as menus

repo.carregar_json()

def _buscar_e_exibir():
    equipamento = menus.buscar_ativo()
    if equipamento:
        print(equipamento)
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
    print("   GERENCIADOR DE EQUIPAMENTOS")
    print("=" * 35)
    print("""
Equipamentos---------------------------
1 - Cadastrar equipamento
2 - Buscar equipamento
3 - Atualizar equipamento
4 - Remover equipamento
5 - Listar equipamentos
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