import json
import os
from Ativo import Ativo, TipoAtivo
from Vulne import Vulnerabilidade

ARQUIVO = "ativos.json"

lista           = []
indice_id       = {}
indice_hostname = {}

def _indexar(ativo):
    indice_id[ativo.id] = ativo
    indice_hostname[ativo.hostname.lower()] = ativo

def _desindexar(ativo):
    indice_id.pop(ativo.id, None)
    indice_hostname.pop(ativo.hostname.lower(), None)

def _reindexar():
    indice_id.clear()
    indice_hostname.clear()
    for a in lista:
        _indexar(a)

def salvar_json():
    dados = [ativo.to_dict() for ativo in lista]
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_json():
    global lista
    if not os.path.exists(ARQUIVO):
        lista = []
        return

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    ativos = []
    for item in dados:
        try:
            tipo_enum = TipoAtivo[item.get("Tipo", "NOTEBOOK")]
        except KeyError:
            tipo_enum = TipoAtivo.NOTEBOOK

        vulnerabilidades = [
            Vulnerabilidade(
                v["descricao"], v["categoria"],
                v["severidade"], v.get("status", "Aberta")
            )
            if isinstance(v, dict)
            else Vulnerabilidade(v, "Desconhecida", "Baixa")
            for v in item.get("Vulnerabilidades", [])
        ]

        ativos.append(Ativo(
            item["Id"],
            item["Hostname"],
            item.get("Responsavel", item.get("Responsável")),
            item["Setor"],
            tipo_enum,
            vulnerabilidades
        ))

    lista = ativos
    _reindexar()