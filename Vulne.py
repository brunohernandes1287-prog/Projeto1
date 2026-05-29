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