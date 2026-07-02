import Repositorio as repo
from Ativo import criar_equipamento
from Vulne import Vulnerabilidade
from Ajudantes import (
    limpar, pausar, input_obrigatorio,
    escolher_tipo, escolher_dado_especifico,
    escolher_dificuldade, escolher_categoria
)


def buscar_ativo(termo=None):
    if not termo:
        termo = input("Digite o hostname ou ID: ").strip()
    if not termo:
        print("⚠️ Campo não pode ser vazio.")
        pausar()
        return None

    if termo.isdigit():
        equipamento = repo.indice_id.get(int(termo))
        if equipamento:
            return equipamento

    equipamento = repo.indice_hostname.get(termo.lower())
    if equipamento:
        return equipamento

    print("\n⚠️ Ativo não encontrado.")
    pausar()
    return None


def cadastrar_ativo():
    limpar()
    print("=" * 35)
    print("      CADASTRAR EQUIPAMENTO")
    print("=" * 35)

    id_novo     = max((e.id for e in repo.lista), default=0) + 1
    hostname    = input_obrigatorio("Hostname")
    responsavel = input_obrigatorio("Responsavel")
    setor       = input_obrigatorio("Setor")

    if hostname.lower() in repo.indice_hostname:
        print(f"\n⚠️ Hostname '{hostname}' já existe.")
        pausar()
        return

    tipo  = escolher_tipo()
    extra = escolher_dado_especifico(tipo)

    equipamento = criar_equipamento(tipo, id_novo, hostname, responsavel, setor, extra)

    repo.lista.append(equipamento)
    repo._indexar(equipamento)
    repo.salvar_json()
    print(f"\n✅ Equipamento cadastrado com ID {id_novo} e Hostname: {hostname}.")
    pausar()
    limpar()
    if input("Deseja adicionar vulnerabilidade? S/N: ").lower() == 's':
        adicionar_vulnerabilidade(equipamento)


def atualizar_ativo():
    limpar()
    print("=" * 35)
    print("      ATUALIZAR EQUIPAMENTO")
    print("=" * 35)

    equipamento = buscar_ativo()
    if not equipamento:
        return

    equipamento.responsavel = input(f"Novo Responsavel [{equipamento.responsavel}]: ") or equipamento.responsavel
    equipamento.setor       = input(f"Novo Setor [{equipamento.setor}]: ") or equipamento.setor

    repo.salvar_json()
    print("\n✅ Equipamento atualizado com sucesso.")
    pausar()


def remover_ativo():
    limpar()
    print("=" * 35)
    print("      REMOVER EQUIPAMENTO")
    print("=" * 35)

    equipamento = buscar_ativo()
    if equipamento and input("Confirma remoção? S/N: ").lower() == 's':
        repo._desindexar(equipamento)
        repo.lista.remove(equipamento)
        repo.salvar_json()
        print(f"\n🗑️ Equipamento '{equipamento.hostname}' removido.")
    pausar()


def listar_ativos():
    limpar()
    print("=" * 35)
    print("      LISTA DE EQUIPAMENTOS")
    print("=" * 35)

    if not repo.lista:
        print("\nNenhum equipamento cadastrado.")
        pausar()
    else:
        for equipamento in repo.lista:
            print(equipamento)
            print("-" * 35)
    input("\nPressione Enter para voltar...")


def adicionar_vulnerabilidade(equipamento=None):
    limpar()
    print("=" * 35)
    print(" ADICIONAR VULNERABILIDADE")
    print("=" * 35)

    if not equipamento:
        equipamento = buscar_ativo()
    if not equipamento:
        print("\n⚠️ Equipamento não encontrado.")
        pausar()
        return

    while True:
        nome       = input_obrigatorio("Vulnerabilidade")
        severidade = escolher_dificuldade()
        categoria  = escolher_categoria()
        vuln       = Vulnerabilidade(nome, categoria, severidade)
        equipamento.vulnerabilidades.append(vuln)
        repo.salvar_json()
        print("\n✅ Vulnerabilidade adicionada.")

        if input("Deseja adicionar outra? S/N: ").lower() != 's':
            break


def ver_vulnerabilidades():
    limpar()
    print("=" * 35)
    print("   VER VULNERABILIDADES")
    print("=" * 35)

    equipamento = buscar_ativo()
    if equipamento:
        if equipamento.vulnerabilidades:
            print(f"\n📋 Vulnerabilidades de {equipamento.hostname}:\n")
            for v in equipamento.vulnerabilidades:
                print(f"  - {v}")
        else:
            print("\nNenhuma vulnerabilidade cadastrada.")
    input("\nPressione Enter para voltar...")


def consertar_vulnerabilidade():
    limpar()
    print("=" * 35)
    print(" CONSERTAR VULNERABILIDADE")
    print("=" * 35)

    equipamento = buscar_ativo()
    if not equipamento:
        return

    if not equipamento.vulnerabilidades:
        print("\nNenhuma vulnerabilidade cadastrada.")
        pausar()
        return

    for i, v in enumerate(equipamento.vulnerabilidades, 1):
        print(f"\n{i} - {v}")

    try:
        escolha = int(input("\nEscolha a vulnerabilidade: "))
        if not (1 <= escolha <= len(equipamento.vulnerabilidades)):
            raise ValueError

        vuln = equipamento.vulnerabilidades[escolha - 1]
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