import json
import time
import os
from enum import Enum
 
ARQUIVO = "ativos.json"
 
class TipoAtivo(Enum):
    NOTEBOOK         = 1
    SERVIDOR         = 2
    ROTEADOR         = 3
    SOFTWARE         = 4
    APLICACAO_WEB    = 5
    BANCO_DE_DADOS   = 6
    IMPRESSORA       = 7
    ESTACAO_TRABALHO = 8
 
class Vulnerabilidade:
   CATEGORIAS = {
       "1": "Injeção",
       "2": "Autenticacao",
       "3": "Configuração",
       "4": "Criptografia",
       "5": "Controle de Acesso",
       "6": "Exposição de Dados",
       "7": "Outro"
   }
   STATUS_OPCOES = {
        "1": "Aberta",
        "2": "Em tratamento",
        "3": "Corrigida",
        "4": "Aceita como risco"
    }
   def __init__(self, descricao, categoria, severidade, status="Aberta"):
        self.descricao  = descricao
        self.categoria  = categoria
        self.severidade = severidade
        self.status     = status
   def to_dict(self):
        return {
            "descricao":  self.descricao,
            "categoria":  self.categoria,
            "severidade": self.severidade,
            "status":     self.status
        }
   def __str__(self):
        return (
            f"Descrição : {self.descricao}\n"
            f"   Categoria : {self.categoria}\n"
            f"   Severidade: {self.severidade}\n"
            f"   Status    : {self.status}"
        )
 
 
class Ativo:
    def __init__(self, id, hostname, responsavel, setor, tipo, vulnerabilidades):
        self.id = id
        self.hostname = hostname
        self.responsavel = responsavel
        self.setor = setor
        self.tipo = tipo
        self.vulnerabilidades = vulnerabilidades if vulnerabilidades is not None else []
 
    def to_dict(self):
        return {
            "Id": self.id,
            "Hostname": self.hostname,
            "Responsavel": self.responsavel,
            "Setor": self.setor,
            "Tipo": self.tipo.name,
            "Vulnerabilidades": [v.to_dict() for v in self.vulnerabilidades]
        }
 
    def __str__(self):
        if self.vulnerabilidades:
            vulns = ""
            for i, v in enumerate(self.vulnerabilidades, 1):
                vulns += f"\n  [{i}]  {v}\n"
        else:
            vulns = "\n   Nenhuma Vulnerabilidade registrada."
 
        return (
            f"\n{'=' * 40}\n"
            f"  ID          : {self.id}\n"
            f"  Hostname    : {self.hostname}\n"
            f"  Responsavel : {self.responsavel}\n"
            f"  Setor       : {self.setor}\n"
            f"  Tipo        : {self.tipo.name} (código {self.tipo.value})\n"
            f"  Vulnerabilidades:{vulns}"
            f"{'=' * 40}"
        )
 
indice_id = {}
indice_hostname = {}
 
def _indexar(ativo):
    indice_id[ativo.id] = ativo
    indice_hostname[ativo.hostname.lower()] = ativo
 
def _desindexar(ativo):
    indice_id.pop(ativo.id, None)
    indice_hostname.pop(ativo.hostname.lower(), None)
 
def salvar_json():
    dados = [ativo.to_dict() for ativo in lista]
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
 
def _reindexar():
    indice_id.clear()
    indice_hostname.clear()
    for a in lista:
        _indexar(a)

def carregar_json():
    if not os.path.exists(ARQUIVO):
        return []
 
    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
 
    ativos = []
 
    for item in dados:
        tipo_salvo = item.get("Tipo", "NOTEBOOK")
 
        try:
            tipo_enum = TipoAtivo[tipo_salvo]
        except KeyError:
            tipo_enum = TipoAtivo.NOTEBOOK
 
        vulnerabilidades = []
        for v in item.get("Vulnerabilidades", []):
            if isinstance(v, dict):
                vulnerabilidades.append(
                    Vulnerabilidade(
                        v["descricao"],
                        v["categoria"],
                        v["severidade"],
                        v.get("status", "Aberta")
                    )
                )
            else:
                vulnerabilidades.append(Vulnerabilidade(v, "Desconhecida", "Baixa"))
 
        ativo = Ativo(
            item["Id"],
            item["Hostname"],
            item.get("Responsavel", item.get("Responsável")),
            item["Setor"],
            tipo_enum,
            vulnerabilidades
        )
 
        ativos.append(ativo)
 
    return ativos
 
 
def escolher_tipo():
    print("\nTipos de Ativo:")
    print("1 - Notebook")
    print("2 - Servidor")
    print("3 - Roteador")
    print("4 - Software")  
    print("5 - APLICACAO_WEB")   
    print("6 - BANCO_DE_DADOS")  
    print("7 - IMPRESSORA")     
    print("8 - ESTACAO_TRABALHO") 
    while True:
        try:
            codigo = int(input("\nEscolha o tipo: "))
            return TipoAtivo(codigo)
        except ValueError:
            print("⚠️ Digite um número válido.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
        except Exception:
            print("⚠️ Escolha um tipo existente.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
 
 
def escolher_dificuldade():
    opcoes = {"1": "Baixa", "2": "Média", "3": "Alta", "4": "Crítica"}
 
    print("\nDificuldade:")
    print("1 - Baixa")
    print("2 - Média")
    print("3 - Alta")
    print("4 - Crítica")
 
    while True:
        escolha = input("\nEscolha: ")
        if escolha in opcoes:
            return opcoes[escolha]
        print("⚠️ Escolha uma opção válida.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
 
def input_obrigatorio(campo):
    while True:
        valor = input(f"{campo}: ").strip()
        if valor:
            return valor
        print(f"⚠️ {campo} não pode ser vazio.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")

def cadastrar_ativo():
    os.system("cls" if os.name == "nt" else "clear")
 
    print("=" * 35)
    print("      CADASTRAR ATIVO")
    print("=" * 35)
 
    id_novo = max([ativo.id for ativo in lista], default=0) + 1
 
    hostname    = input_obrigatorio("Hostname")
    responsavel = input_obrigatorio("Responsavel")
    setor       = input_obrigatorio("Setor")

    if hostname.lower() in indice_hostname:
            print(f"\n⚠️ Já existe um ativo com o hostname '{hostname}'.")
            time.sleep(2)
            return
    tipo = escolher_tipo()
 
    ativo = Ativo(id_novo, hostname, responsavel, setor, tipo, [])
 
    lista.append(ativo)
    _indexar(ativo)   
    salvar_json()
    os.system("cls" if os.name == "nt" else "clear")
    escolha = input("""Deseja adicionar vulnerabilidade S/N
                    """)
    if escolha.lower() == 's':
        adicionar_vulnerabilidade(ativo)
    else:
         print(f"\n✅ Ativo '{hostname}' cadastrado com sucesso.")
    time.sleep(2)
 
def buscar_ativo(termo=None):
    if not termo:
        termo = input("Digite o hostname ou ID: ")
 
    termo = termo.strip()
 
    if not termo:
        print("⚠️ Campo não pode ser vazio.")
        time.sleep(2)
        return None

    if termo.isdigit():
        ativo = indice_id.get(int(termo))
        if ativo:
            return ativo


   
    ativo = indice_hostname.get(termo.lower())
    if ativo:
        return ativo

    print("\n⚠️ Ativo não encontrado.")
    time.sleep(2)

    return None

 
 
def atualizar_ativo():
    os.system("cls" if os.name == "nt" else "clear")
 
    print("=" * 35)
    print("      ATUALIZAR ATIVO")
    print("=" * 35)
 
    ativo = buscar_ativo()
 
    if ativo:
        ativo.responsavel = input(
            f"Novo Responsavel [{ativo.responsavel}]: "
        ) or ativo.responsavel
 
        ativo.setor = input(
            f"Novo Setor [{ativo.setor}]: "
        ) or ativo.setor
 
        print("\nDeseja alterar o tipo?")
        escolha = input("S/N: ").lower()
 
        if escolha == "s":
            ativo.tipo = escolher_tipo()
 
        salvar_json()
        print("\n✅ Ativo atualizado com sucesso.")
    
    time.sleep(2)
 
 
def remover_ativo():
    os.system("cls" if os.name == "nt" else "clear")
 
    print("=" * 35)
    print("       REMOVER ATIVO")
    print("=" * 35)
 
    ativo = buscar_ativo()
 
    if ativo:
        s = input("Deseja realmente remover esse ativo?(S/N)\n")
        if s.lower() == "s":
            _desindexar(ativo)
            lista.remove(ativo)
            salvar_json()
            print(f"\n🗑️ Ativo '{ativo.hostname}' removido.")

    time.sleep(2)
 
def escolher_categoria():
    print("\nCategorias:")
    for k, v in Vulnerabilidade.CATEGORIAS.items():
        print(f"{k} - {v}")

    while True:
        escolha = input("\nEscolha: ")
        if escolha in Vulnerabilidade.CATEGORIAS:
            return Vulnerabilidade.CATEGORIAS[escolha]
        print("⚠️ Escolha uma opção válida.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
def adicionar_vulnerabilidade(ativo=None):
    os.system("cls" if os.name == "nt" else "clear")
 
    print("=" * 35)
    print(" ADICIONAR VULNERABILIDADE")
    print("=" * 35)
 
    if not ativo:
        ativo = buscar_ativo()
 
    if ativo:
        while True:
            nome = input_obrigatorio("Vulnerabilidade")
            dificuldade = escolher_dificuldade()
            categoria = escolher_categoria()
            vuln = Vulnerabilidade(nome, categoria, dificuldade)
            ativo.vulnerabilidades.append(vuln)
            salvar_json()
            print("\n✅ Vulnerabilidade adicionada.")
        
            escolha = input("Deseja adicionar outra? S/N: ")
            if escolha.lower() != 's':
                break   
    else:
        print("\n⚠️ Ativo não encontrado.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
    
    
    
 
 
def ver_vulnerabilidades():
    os.system("cls" if os.name == "nt" else "clear")
 
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
    os.system("cls" if os.name == "nt" else "clear")
 
    print("=" * 35)
    print(" CONSERTAR VULNERABILIDADE")
    print("=" * 35)
 
    ativo = buscar_ativo()
 
    if ativo:
        if not ativo.vulnerabilidades:
            print("\nNenhuma vulnerabilidade cadastrada.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            
            return
 
        print()
        for indice, vuln in enumerate(ativo.vulnerabilidades, start=1):
            print(f"{indice} - {vuln}")
 
        try:
            escolha = int(input("\nEscolha a vulnerabilidade: "))
 
            if 1 <= escolha <= len(ativo.vulnerabilidades):
                vuln = ativo.vulnerabilidades[escolha - 1]
                print("\nEscolha o novo status:")
                for k, v in Vulnerabilidade.STATUS_OPCOES.items():
                    print(f"{k} - {v}")

                escolha_status = input("\nEscolha: ")

                if escolha_status in Vulnerabilidade.STATUS_OPCOES:
                        vuln.status = Vulnerabilidade.STATUS_OPCOES[escolha_status]
                        salvar_json()
                        print(f"\n✅ '{vuln.descricao}' marcada como '{vuln.status}'.")
                else:
                        print("\n⚠️ Opção inválida.")
                        time.sleep(2)
                        os.system("cls" if os.name == "nt" else "clear")
            else:
                print("\n⚠️ Número inválido.")
                time.sleep(2)
                os.system("cls" if os.name == "nt" else "clear")
 
        except ValueError:
            print("\n⚠️ Digite um número válido.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
    else:
        print("\n⚠️ Ativo não encontrado.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
 
    time.sleep(2)
 
 
def listar_ativos():
    os.system("cls" if os.name == "nt" else "clear")
 
    print("=" * 35)
    print("       LISTA DE ATIVOS")
    print("=" * 35)
 
    if not lista:
        print("\nNenhum ativo cadastrado.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
    else:
        for ativo in lista:
            print(ativo)
            print("-" * 35)
 
    input("\nPressione Enter para voltar...")
 
 
lista = carregar_json()
_reindexar()
 
while True:
    os.system("cls" if os.name == "nt" else "clear")
 
    print("=" * 35)
    print("   GERENCIADOR DE ATIVOS")
    print("=" * 35)
 
    try:
        opcao = int(input("""
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
 
 
Escolha uma opcao: """))
 
    except ValueError:
        print("\n⚠️ Digite um número válido.")
        time.sleep(2)
        continue
 
    if opcao == 0:
        print("\nSaindo...")
        break
 
    elif opcao == 1:
        cadastrar_ativo()
 
    elif opcao == 2:
        os.system("cls" if os.name == "nt" else "clear")
        ativo_encontrado = buscar_ativo()
 
        if ativo_encontrado:
            print(ativo_encontrado)
        else:
            print("\n⚠️ Ativo não encontrado.")
 
        input("\nPressione Enter para voltar...")
 
    elif opcao == 3:
        atualizar_ativo()
 
    elif opcao == 4:
        remover_ativo()
 
    elif opcao == 6:
        adicionar_vulnerabilidade()
 
    elif opcao == 7:
        ver_vulnerabilidades()
 
    elif opcao == 8:
        consertar_vulnerabilidade()
 
    elif opcao == 5:
        listar_ativos()
 
    else:
        print("\n⚠️ Opcao inválida.")
        time.sleep(2)
 

