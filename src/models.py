# =============================================================
# models.py — Entidade de domínio do sistema
# =============================================================


class Task:
    """
    Representa uma tarefa no quadro Kanban.
    """

    # Status possíveis
    STATUS_TODO = "To Do"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_DONE = "Done"

    # Categorias possíveis
    CATEGORIA_FACULDADE = "Faculdade"
    CATEGORIA_TRABALHO = "Trabalho"
    CATEGORIA_PESSOAL = "Pessoal"
    CATEGORIA_OUTROS = "Outros"

    def __init__(
        self,
        titulo: str,
        descricao: str,
        prioridade: str,
        categoria: str = "Outros",
        data_limite: str = ""
    ):
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.categoria = categoria
        self.data_limite = data_limite

        # Toda tarefa começa em To Do
        self.status = self.STATUS_TODO

        # Histórico inicial
        self.historico = [
            "Tarefa criada"
        ]

    # ----------------------------------------------------------
    # Alteração de status
    # ----------------------------------------------------------

    def _alterar_status(self, novo_status: str) -> None:
        """
        Altera o status da tarefa e registra a mudança no histórico.
        """

        status_anterior = self.status

        self.status = novo_status

        self.historico.append(
            f"Status alterado de {status_anterior} "
            f"para {self.status}"
        )

    # ----------------------------------------------------------
    # Transições de estado
    # ----------------------------------------------------------

    def iniciar(self) -> None:
        """Move a tarefa para In Progress."""

        self._alterar_status(
            self.STATUS_IN_PROGRESS
        )

    def concluir(self) -> None:
        """Move a tarefa para Done."""

        self._alterar_status(
            self.STATUS_DONE
        )

    # ----------------------------------------------------------
    # Conversão para dicionário
    # ----------------------------------------------------------

    def to_dict(self) -> dict:

        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "prioridade": self.prioridade,
            "categoria": self.categoria,
            "data_limite": self.data_limite,
            "status": self.status,
            "historico": self.historico
        }

    # ----------------------------------------------------------
    # Conversão do dicionário para Task
    # ----------------------------------------------------------

    @classmethod
    def from_dict(cls, dados: dict):

        tarefa = cls(
            dados.get("titulo", ""),
            dados.get("descricao", ""),
            dados.get("prioridade", "Baixa"),
            dados.get("categoria", "Outros"),
            dados.get("data_limite", "")
        )

        tarefa.status = dados.get(
            "status",
            cls.STATUS_TODO
        )

        tarefa.historico = dados.get(
            "historico",
            ["Tarefa criada"]
        )

        return tarefa

    # ----------------------------------------------------------
    # Representação textual
    # ----------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"Task(titulo={self.titulo!r}, "
            f"prioridade={self.prioridade!r}, "
            f"categoria={self.categoria!r}, "
            f"data_limite={self.data_limite!r}, "
            f"status={self.status!r})"
        )