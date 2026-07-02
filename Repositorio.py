import json
import os
from Ativo import Equipamento, Notebook, Servidor, Impressora, TipoAtivo
from Vulne import Vulnerabilidade

ARQUIVO = "ativos.json"

lista           = []
indice_id       = {}
indice_hostname = {}


def _indexar(equipamento):
    indice_id[equipamento.id] = equipamento
    indice_hostname[equipamento.hostname.lower()] = equipamento


def _desindexar(equipamento):
    indice_id.pop(equipamento.id, None)
    indice_hostname.pop(equipamento.hostname.lower(), None)


def _reindexar():
    indice_id.clear()
    indice_hostname.clear()
    for e in lista:
        _indexar(e)


def salvar_json():
    dados = [equipamento.to_dict() for equipamento in lista]
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def _montar_vulnerabilidades(item):
    return [
        Vulnerabilidade(
            v["descricao"], v["categoria"],
            v["severidade"], v.get("status", "Aberta")
        )
        for v in item.get("Vulnerabilidades", [])
    ]


def _criar_a_partir_do_dict(item):
    try:
        tipo_enum = TipoAtivo[item.get("Tipo", "NOTEBOOK")]
    except KeyError:
        tipo_enum = TipoAtivo.NOTEBOOK

    vulnerabilidades = _montar_vulnerabilidades(item)
    id_         = item["Id"]
    hostname    = item["Hostname"]
    responsavel = item.get("Responsavel", item.get("Responsável", ""))
    setor       = item["Setor"]
    # Fallback: se o JSON não tem "Classe" (formato antigo), deduz pela "Tipo"
    mapa_tipo_classe = {
        TipoAtivo.NOTEBOOK: "Notebook",
        TipoAtivo.SERVIDOR: "Servidor",
        TipoAtivo.IMPRESSORA: "Impressora",
    }
    classe = item.get("Classe") or mapa_tipo_classe.get(tipo_enum, "Equipamento")

    if classe == "Notebook":
        return Notebook(id_, hostname, responsavel, setor,
                         item.get("SistemaOperacional", ""), vulnerabilidades)
    elif classe == "Servidor":
        return Servidor(id_, hostname, responsavel, setor,
                         item.get("IP", ""), vulnerabilidades)
    elif classe == "Impressora":
        return Impressora(id_, hostname, responsavel, setor,
                           item.get("Modelo", ""), vulnerabilidades)
    else:
        return Equipamento(id_, hostname, responsavel, setor, tipo_enum, vulnerabilidades)


def carregar_json():
    global lista
    if not os.path.exists(ARQUIVO):
        lista = []
        return

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    lista = [_criar_a_partir_do_dict(item) for item in dados]
    _reindexar()