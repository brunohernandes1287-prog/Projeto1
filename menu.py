import Repositorio as repo
from Ativo import Ativo
from Vulne import Vulnerabilidade
from Ajudantes import (
    limpar, pausar, input_obrigatorio,
    escolher_tipo, escolher_dificuldade, escolher_categoria
)

def buscar_ativo(termo=None):
    if not termo:
        termo = input("Digite o hostname ou ID: ").strip()
    if not termo:
        print("⚠️ Campo não pode ser vazio.")
        pausar()
        return None

    if termo.isdigit():
        ativo = repo.indice_id.get(int(termo))
        if ativo:
            return ativo

    ativo = repo.indice_hostname.get(termo.lower())
    if ativo:
        return ativo

    print("\n⚠️ Ativo não encontrado.")
    pausar()
    return None

def cadastrar_ativo():
    limpar()
    print("=" * 35)
    print("      CADASTRAR ATIVO")
    print("=" * 35)

    id_novo     = max((a.id for a in repo.lista), default=0) + 1
    hostname    = input_obrigatorio("Hostname")
    responsavel = input_obrigatorio("Responsavel")
    setor       = input_obrigatorio("Setor")

    if hostname.lower() in repo.indice_hostname:
        print(f"\n⚠️ Hostname '{hostname}' já existe.")
        pausar()
        return

    tipo  = escolher_tipo()
    ativo = Ativo(id_novo, hostname, responsavel, setor, tipo, [])

    repo.lista.append(ativo)
    repo._indexar(ativo)
    repo.salvar_json()
    print(f"\n✅ Ativo cadastrado com ID {id_novo} e Hostname: {hostname}.")
    pausar()
    limpar()
    if input("Deseja adicionar vulnerabilidade? S/N: ").lower() == 's':
        adicionar_vulnerabilidade(ativo)
    

def atualizar_ativo():
    limpar()
    print("=" * 35)
    print("      ATUALIZAR ATIVO")
    print("=" * 35)

    ativo = buscar_ativo()
    if not ativo:
        return

    ativo.responsavel = input(f"Novo Responsavel [{ativo.responsavel}]: ") or ativo.responsavel
    ativo.setor       = input(f"Novo Setor [{ativo.setor}]: ") or ativo.setor

    if input("\nDeseja alterar o tipo? S/N: ").lower() == 's':
        ativo.tipo = escolher_tipo()

    repo.salvar_json()
    print("\n✅ Ativo atualizado com sucesso.")
    pausar()

def remover_ativo():
    limpar()
    print("=" * 35)
    print("       REMOVER ATIVO")
    print("=" * 35)

    ativo = buscar_ativo()
    if ativo and input("Confirma remoção? S/N: ").lower() == 's':
        repo._desindexar(ativo)
        repo.lista.remove(ativo)
        repo.salvar_json()
        print(f"\n🗑️ Ativo '{ativo.hostname}' removido.")
    pausar()

def listar_ativos():
    limpar()
    print("=" * 35)
    print("       LISTA DE ATIVOS")
    print("=" * 35)

    if not repo.lista:
        print("\nNenhum ativo cadastrado.")
        pausar()
    else:
        for ativo in repo.lista:
            print(ativo)
            print("-" * 35)
    input("\nPressione Enter para voltar...")

def adicionar_vulnerabilidade(ativo=None):
    limpar()
    print("=" * 35)
    print(" ADICIONAR VULNERABILIDADE")
    print("=" * 35)

    if not ativo:
        ativo = buscar_ativo()
    if not ativo:
        print("\n⚠️ Ativo não encontrado.")
        pausar()
        return

    while True:
        nome       = input_obrigatorio("Vulnerabilidade")
        severidade = escolher_dificuldade()
        categoria  = escolher_categoria()
        vuln       = Vulnerabilidade(nome, categoria, severidade)
        ativo.vulnerabilidades.append(vuln)
        repo.salvar_json()
        print("\n✅ Vulnerabilidade adicionada.")

        if input("Deseja adicionar outra? S/N: ").lower() != 's':
            break

def ver_vulnerabilidades():
    limpar()
    print("=" * 35)
    print("   VER VULNERABILIDADES")
    print("=" * 35)

    ativo = buscar_ativo()
    if ativo:
        if ativo.vulnerabilidades:
            print(f"\n📋 Vulnerabilidades de {ativo.hostname}:\n")
            for v in ativo.vulnerabilidades:
                print(f"  - {v}")
        else:
            print("\nNenhuma vulnerabilidade cadastrada.")
    input("\nPressione Enter para voltar...")

def consertar_vulnerabilidade():
    limpar()
    print("=" * 35)
    print(" CONSERTAR VULNERABILIDADE")
    print("=" * 35)

    ativo = buscar_ativo()
    if not ativo:
        return

    if not ativo.vulnerabilidades:
        print("\nNenhuma vulnerabilidade cadastrada.")
        pausar()
        return

    for i, v in enumerate(ativo.vulnerabilidades, 1):
        print(f"\n{i} - {v}")

    try:
        escolha = int(input("\nEscolha a vulnerabilidade: "))
        if not (1 <= escolha <= len(ativo.vulnerabilidades)):
            raise ValueError

        vuln = ativo.vulnerabilidades[escolha - 1]
        print("\nNovo status:")
        for k, v in Vulnerabilidade.STATUS_OPCOES.items():
            print(f"{k} - {v}")

        s = input("\nEscolha: ")
        if s in Vulnerabilidade.STATUS_OPCOES:
            vuln.status = Vulnerabilidade.STATUS_OPCOES[s]
            repo.salvar_json()
            print(f"\n✅ '{vuln.descricao}' → '{vuln.status}'.")
        else:
            print("\n⚠️ Opção inválida.")

    except ValueError:
        print("\n⚠️ Número inválido.")

    pausar()