from enum import Enum
from Vulne import Vulnerabilidade

class TipoAtivo(Enum):
    NOTEBOOK         = 1
    SERVIDOR         = 2
    ROTEADOR         = 3
    SOFTWARE         = 4
    APLICACAO_WEB    = 5
    BANCO_DE_DADOS   = 6
    IMPRESSORA       = 7
    ESTACAO_TRABALHO = 8

class Ativo:
    def __init__(self, id, hostname, responsavel, setor, tipo, vulnerabilidades):
        self.id               = id
        self.hostname         = hostname
        self.responsavel      = responsavel
        self.setor            = setor
        self.tipo             = tipo
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