from enum import Enum


class TipoAtivo(Enum):
    NOTEBOOK         = 1
    SERVIDOR         = 2
    ROTEADOR         = 3
    SOFTWARE         = 4
    APLICACAO_WEB    = 5
    BANCO_DE_DADOS   = 6
    IMPRESSORA       = 7
    ESTACAO_TRABALHO = 8


class Equipamento:
    def __init__(self, id, hostname, responsavel, setor, tipo, vulnerabilidades=None):
        self.id               = id
        self.hostname         = hostname
        self.responsavel      = responsavel
        self.setor            = setor
        self.tipo             = tipo
        self.vulnerabilidades = vulnerabilidades if vulnerabilidades is not None else []

    def info_especifica(self):
        return "Sem informações adicionais"

    def dados_especificos(self):
        return {}

    def to_dict(self):
        return {
            "Id": self.id,
            "Hostname": self.hostname,
            "Responsavel": self.responsavel,
            "Setor": self.setor,
            "Tipo": self.tipo.name,
            "Classe": type(self).__name__,
            "Vulnerabilidades": [v.to_dict() for v in self.vulnerabilidades],
            **self.dados_especificos()
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
            f"  Tipo        : {self.tipo.name} ({type(self).__name__})\n"
            f"  {self.info_especifica()}\n"
            f"  Vulnerabilidades:{vulns}"
            f"{'=' * 40}"
        )


class Notebook(Equipamento):
    def __init__(self, id, hostname, responsavel, setor, sistema_operacional, vulnerabilidades=None):
        super().__init__(id, hostname, responsavel, setor, TipoAtivo.NOTEBOOK, vulnerabilidades)
        self.sistema_operacional = sistema_operacional

    def info_especifica(self):
        return f"Sistema Operacional: {self.sistema_operacional}"

    def dados_especificos(self):
        return {"SistemaOperacional": self.sistema_operacional}


class Servidor(Equipamento):
    def __init__(self, id, hostname, responsavel, setor, ip, vulnerabilidades=None):
        super().__init__(id, hostname, responsavel, setor, TipoAtivo.SERVIDOR, vulnerabilidades)
        self.ip = ip

    def info_especifica(self):
        return f"IP: {self.ip}"

    def dados_especificos(self):
        return {"IP": self.ip}


class Impressora(Equipamento):
    def __init__(self, id, hostname, responsavel, setor, modelo, vulnerabilidades=None):
        super().__init__(id, hostname, responsavel, setor, TipoAtivo.IMPRESSORA, vulnerabilidades)
        self.modelo = modelo

    def info_especifica(self):
        return f"Modelo: {self.modelo}"

    def dados_especificos(self):
        return {"Modelo": self.modelo}


def criar_equipamento(tipo, id, hostname, responsavel, setor, extra=None, vulnerabilidades=None):
    """Fábrica: decide qual classe instanciar de acordo com o tipo escolhido."""
    if tipo == TipoAtivo.NOTEBOOK:
        return Notebook(id, hostname, responsavel, setor, extra, vulnerabilidades)
    elif tipo == TipoAtivo.SERVIDOR:
        return Servidor(id, hostname, responsavel, setor, extra, vulnerabilidades)
    elif tipo == TipoAtivo.IMPRESSORA:
        return Impressora(id, hostname, responsavel, setor, extra, vulnerabilidades)
    else:
        return Equipamento(id, hostname, responsavel, setor, tipo, vulnerabilidades)