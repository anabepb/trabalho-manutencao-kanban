import json
from pathlib import Path

from src.models import Task


ARQUIVO_DADOS = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "tarefas.json"
)


def carregar_tarefas() -> list[Task]:
    if not ARQUIVO_DADOS.exists():
        return []

    try:
        with open(
            ARQUIVO_DADOS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        return [
            Task.from_dict(item)
            for item in dados
        ]

    except (json.JSONDecodeError, OSError):
        return []


def salvar_tarefas(tarefas: list[Task]) -> None:
    ARQUIVO_DADOS.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        ARQUIVO_DADOS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            [
                tarefa.to_dict()
                for tarefa in tarefas
            ],
            arquivo,
            ensure_ascii=False,
            indent=4
        )
    