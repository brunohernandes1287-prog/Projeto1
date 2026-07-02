import os
import time


def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def pausar(segundos=2):
    time.sleep(segundos)


def input_obrigatorio(campo):
    while True:
        valor = input(f"{campo}: ").strip()
        if valor:
            return valor
        print(f"⚠️ {campo} não pode ser vazio.")
        pausar()
        limpar()


def escolher_tipo():
    from Ativo import TipoAtivo
    print("\nTipos de Equipamento:")
    for t in TipoAtivo:
        print(f"{t.value} - {t.name}")
    while True:
        try:
            return TipoAtivo(int(input("\nEscolha o tipo: ")))
        except (ValueError, KeyError):
            print("⚠️ Escolha um tipo válido.")
            pausar(); limpar()


def escolher_dado_especifico(tipo):
    """Pergunta o campo extra específico, conforme o tipo escolhido."""
    from Ativo import TipoAtivo
    if tipo == TipoAtivo.NOTEBOOK:
        return input_obrigatorio("Sistema Operacional")
    elif tipo == TipoAtivo.SERVIDOR:
        return input_obrigatorio("Endereço IP")
    elif tipo == TipoAtivo.IMPRESSORA:
        return input_obrigatorio("Modelo")
    return None


def escolher_dificuldade():
    opcoes = {"1": "Baixa", "2": "Média", "3": "Alta", "4": "Crítica"}
    print("\nSeveridade:")
    for k, v in opcoes.items():
        print(f"{k} - {v}")
    while True:
        escolha = input("\nEscolha: ")
        if escolha in opcoes:
            return opcoes[escolha]
        print("⚠️ Opção inválida.")
        pausar(); limpar()


def escolher_categoria():
    from Vulne import Vulnerabilidade
    print("\nCategorias:")
    for k, v in Vulnerabilidade.CATEGORIAS.items():
        print(f"{k} - {v}")
    while True:
        escolha = input("\nEscolha: ")
        if escolha in Vulnerabilidade.CATEGORIAS:
            return Vulnerabilidade.CATEGORIAS[escolha]
        print("⚠️ Opção inválida.")
        pausar(); limpar()