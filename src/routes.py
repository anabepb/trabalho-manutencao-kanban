# =============================================================
# routes.py — Rotas HTTP e interface do sistema Kanban
# =============================================================

import json
from pathlib import Path

from flask import render_template_string, request, redirect
from src.models import Task


# =============================================================
# Persistência em JSON
# =============================================================

ARQUIVO_DADOS = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "tarefas.json"
)


def carregar_tarefas() -> list[Task]:
    """
    Carrega as tarefas salvas no arquivo JSON.
    """

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

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def salvar_tarefas() -> None:
    """
    Salva todas as tarefas no arquivo JSON.
    """

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


# Carrega as tarefas quando o programa é iniciado
tarefas: list[Task] = carregar_tarefas()


# =============================================================
# Página principal
# =============================================================

HTML = """
<!DOCTYPE html>

<html lang="pt-br">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Kanban Task Manager</title>


    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }


        body {

            min-height: 100vh;

            background: linear-gradient(
                135deg,
                #14001f,
                #2d1148,
                #4b1f73,
                #6d28d9
            );

            color: white;

            padding: 40px;
        }


        h1 {

            text-align: center;

            margin-bottom: 35px;

            font-size: 48px;

            color: #f5e9ff;
        }


        .container {

            max-width: 1500px;

            margin: auto;
        }


        /* ================================================== */
        /* FORMULÁRIO                                         */
        /* ================================================== */


        form {

            background:
                rgba(255, 255, 255, 0.08);

            border:
                1px solid
                rgba(255, 255, 255, 0.12);

            border-radius: 28px;

            padding: 25px;

            margin-bottom: 40px;

            display: flex;

            gap: 15px;

            flex-wrap: wrap;
        }


        input,
        select {

            flex: 1;

            min-width: 180px;

            padding: 16px;

            border: none;

            outline: none;

            border-radius: 18px;

            background:
                rgba(255, 255, 255, 0.12);

            color: white;

            font-size: 15px;
        }


        input::placeholder {

            color: #ccc;
        }


        select option {

            background: #2d1148;

            color: white;
        }


        button {

            padding: 16px 28px;

            border: none;

            border-radius: 18px;

            background: linear-gradient(
                135deg,
                #c084fc,
                #9333ea
            );

            color: white;

            font-weight: bold;

            cursor: pointer;
        }


        /* ================================================== */
        /* KANBAN                                             */
        /* ================================================== */


        .kanban {

            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 25px;
        }


        .column {

            background:
                rgba(255, 255, 255, 0.08);

            border-radius: 28px;

            padding: 22px;

            min-height: 600px;

            border:
                1px solid
                rgba(255, 255, 255, 0.12);
        }


        .column h2 {

            text-align: center;

            margin-bottom: 25px;

            font-size: 26px;

            color: #f3d9ff;
        }


        .column-count {

            display: inline-block;

            background:
                rgba(255, 255, 255, 0.15);

            border-radius: 20px;

            padding: 2px 10px;

            font-size: 14px;
        }


        /* ================================================== */
        /* TAREFAS                                            */
        /* ================================================== */


        .task {

            background:
                rgba(255, 255, 255, 0.10);

            border-radius: 22px;

            padding: 20px;

            margin-bottom: 20px;

            border:
                1px solid
                rgba(255, 255, 255, 0.08);
        }


        .titulo {

            font-size: 18px;

            font-weight: bold;

            margin-bottom: 8px;
        }


        .descricao {

            color: #e9d5ff;

            margin-bottom: 14px;

            font-size: 14px;
        }


        /* ================================================== */
        /* BADGES                                             */
        /* ================================================== */


        .badge {

            display: inline-block;

            margin-right: 6px;

            margin-bottom: 10px;

            padding: 5px 12px;

            border-radius: 12px;

            font-size: 13px;

            font-weight: 600;
        }


        .badge-alta {

            background:
                rgba(244, 63, 94, 0.25);

            color: #fda4af;
        }


        .badge-media {

            background:
                rgba(251, 191, 36, 0.25);

            color: #fde68a;
        }


        .badge-baixa {

            background:
                rgba(34, 197, 94, 0.25);

            color: #86efac;
        }


        .badge-categoria {

            background:
                rgba(59, 130, 246, 0.20);

            color: #bfdbfe;
        }


        /* ================================================== */
        /* PRAZO                                              */
        /* ================================================== */


        .prazo {

            margin-top: 5px;

            margin-bottom: 12px;

            font-size: 13px;

            color: #e9d5ff;
        }


        /* ================================================== */
        /* HISTÓRICO                                          */
        /* ================================================== */


        .historico {

            margin-top: 10px;

            margin-bottom: 15px;

            padding: 10px;

            background:
                rgba(255, 255, 255, 0.06);

            border-radius: 12px;

            font-size: 12px;

            color: #e9d5ff;
        }


        .historico summary {

            cursor: pointer;

            font-weight: bold;
        }


        .historico ul {

            margin-top: 8px;

            padding-left: 20px;
        }


        .historico li {

            margin-bottom: 5px;
        }


        /* ================================================== */
        /* BOTÕES                                             */
        /* ================================================== */


        .buttons {

            display: flex;

            gap: 10px;

            flex-wrap: wrap;
        }


        .btn {

            text-decoration: none;

            padding: 10px 16px;

            border-radius: 14px;

            color: white;

            font-size: 13px;

            font-weight: 600;
        }


        .btn-editar {

            background: #2563eb;
        }


        .btn-iniciar {

            background: #7c3aed;
        }


        .btn-concluir {

            background: #16a34a;
        }


        .btn-excluir {

            background: #e11d48;
        }


        @media (max-width: 1100px) {

            .kanban {

                grid-template-columns: 1fr;
            }
        }

    </style>

</head>


<body>


<div class="container">


    <h1>
        ✨ Kanban Task Manager ✨
    </h1>


    <!-- ================================================== -->
    <!-- NOVA TAREFA                                        -->
    <!-- ================================================== -->


    <form
        method="POST"
        action="/add"
    >


        <input
            type="text"
            name="titulo"
            placeholder="Título da tarefa"
            required
        >


        <input
            type="text"
            name="descricao"
            placeholder="Descrição"
            required
        >


        <select
            name="prioridade"
            required
        >

            <option
                value=""
                disabled
                selected
            >
                🎯 Prioridade
            </option>

            <option value="Alta">
                🔴 Alta
            </option>

            <option value="Média">
                🟡 Média
            </option>

            <option value="Baixa">
                🟢 Baixa
            </option>

        </select>


        <select
            name="categoria"
            required
        >

            <option
                value=""
                disabled
                selected
            >
                📁 Categoria
            </option>

            <option value="Faculdade">
                🎓 Faculdade
            </option>

            <option value="Trabalho">
                💼 Trabalho
            </option>

            <option value="Pessoal">
                🏠 Pessoal
            </option>

            <option value="Outros">
                📌 Outros
            </option>

        </select>


        <input
            type="date"
            name="data_limite"
            required
        >


        <button type="submit">

            + Adicionar Tarefa

        </button>


    </form>


    <!-- ================================================== -->
    <!-- KANBAN                                             -->
    <!-- ================================================== -->


    <div class="kanban">


        <!-- ================================================== -->
        <!-- TO DO                                              -->
        <!-- ================================================== -->


        <div class="column">


            <h2>

                📌 To Do

                <span class="column-count">

                    {{
                        tarefas
                        | selectattr(
                            'status',
                            'equalto',
                            'To Do'
                        )
                        | list
                        | length
                    }}

                </span>

            </h2>


            {% for tarefa in tarefas %}


                {% if tarefa.status == "To Do" %}


                    <div class="task">


                        <div class="titulo">

                            {{ tarefa.titulo }}

                        </div>


                        <div class="descricao">

                            {{ tarefa.descricao }}

                        </div>


                        {% if tarefa.prioridade == "Alta" %}

                            <span class="badge badge-alta">

                                🔴 Alta

                            </span>

                        {% elif tarefa.prioridade == "Média" %}

                            <span class="badge badge-media">

                                🟡 Média

                            </span>

                        {% else %}

                            <span class="badge badge-baixa">

                                🟢 Baixa

                            </span>

                        {% endif %}


                        <span class="badge badge-categoria">

                            📁 {{ tarefa.categoria }}

                        </span>


                        <div class="prazo">

                            📅 Prazo:
                            {{ tarefa.data_limite }}

                        </div>


                        <details class="historico">

                            <summary>

                                📜 Histórico

                            </summary>


                            <ul>

                                {% for evento in tarefa.historico %}

                                    <li>

                                        {{ evento }}

                                    </li>

                                {% endfor %}

                            </ul>


                        </details>


                        <div class="buttons">


                            <a
                                class="btn btn-editar"
                                href="/editar/{{ loop.index0 }}"
                            >

                                ✏️ Editar

                            </a>


                            <a
                                class="btn btn-iniciar"
                                href="/iniciar/{{ loop.index0 }}"
                            >

                                ▶ Iniciar

                            </a>


                            <a
                                class="btn btn-excluir"
                                href="/delete/{{ loop.index0 }}"
                            >

                                🗑 Excluir

                            </a>


                        </div>


                    </div>


                {% endif %}


            {% endfor %}


        </div>


        <!-- ================================================== -->
        <!-- IN PROGRESS                                        -->
        <!-- ================================================== -->


        <div class="column">


            <h2>

                🚀 In Progress

                <span class="column-count">

                    {{
                        tarefas
                        | selectattr(
                            'status',
                            'equalto',
                            'In Progress'
                        )
                        | list
                        | length
                    }}

                </span>

            </h2>


            {% for tarefa in tarefas %}


                {% if tarefa.status == "In Progress" %}


                    <div class="task">


                        <div class="titulo">

                            {{ tarefa.titulo }}

                        </div>


                        <div class="descricao">

                            {{ tarefa.descricao }}

                        </div>


                        {% if tarefa.prioridade == "Alta" %}

                            <span class="badge badge-alta">

                                🔴 Alta

                            </span>

                        {% elif tarefa.prioridade == "Média" %}

                            <span class="badge badge-media">

                                🟡 Média

                            </span>

                        {% else %}

                            <span class="badge badge-baixa">

                                🟢 Baixa

                            </span>

                        {% endif %}


                        <span class="badge badge-categoria">

                            📁 {{ tarefa.categoria }}

                        </span>


                        <div class="prazo">

                            📅 Prazo:
                            {{ tarefa.data_limite }}

                        </div>


                        <details class="historico">

                            <summary>

                                📜 Histórico

                            </summary>


                            <ul>

                                {% for evento in tarefa.historico %}

                                    <li>

                                        {{ evento }}

                                    </li>

                                {% endfor %}

                            </ul>


                        </details>


                        <div class="buttons">


                            <a
                                class="btn btn-editar"
                                href="/editar/{{ loop.index0 }}"
                            >

                                ✏️ Editar

                            </a>


                            <a
                                class="btn btn-concluir"
                                href="/concluir/{{ loop.index0 }}"
                            >

                                ✅ Concluir

                            </a>


                            <a
                                class="btn btn-excluir"
                                href="/delete/{{ loop.index0 }}"
                            >

                                🗑 Excluir

                            </a>


                        </div>


                    </div>


                {% endif %}


            {% endfor %}


        </div>


        <!-- ================================================== -->
        <!-- DONE                                               -->
        <!-- ================================================== -->


        <div class="column">


            <h2>

                ✅ Done

                <span class="column-count">

                    {{
                        tarefas
                        | selectattr(
                            'status',
                            'equalto',
                            'Done'
                        )
                        | list
                        | length
                    }}

                </span>

            </h2>


            {% for tarefa in tarefas %}


                {% if tarefa.status == "Done" %}


                    <div class="task">


                        <div class="titulo">

                            {{ tarefa.titulo }}

                        </div>


                        <div class="descricao">

                            {{ tarefa.descricao }}

                        </div>


                        {% if tarefa.prioridade == "Alta" %}

                            <span class="badge badge-alta">

                                🔴 Alta

                            </span>

                        {% elif tarefa.prioridade == "Média" %}

                            <span class="badge badge-media">

                                🟡 Média

                            </span>

                        {% else %}

                            <span class="badge badge-baixa">

                                🟢 Baixa

                            </span>

                        {% endif %}


                        <span class="badge badge-categoria">

                            📁 {{ tarefa.categoria }}

                        </span>


                        <div class="prazo">

                            📅 Prazo:
                            {{ tarefa.data_limite }}

                        </div>


                        <details class="historico">

                            <summary>

                                📜 Histórico

                            </summary>


                            <ul>

                                {% for evento in tarefa.historico %}

                                    <li>

                                        {{ evento }}

                                    </li>

                                {% endfor %}

                            </ul>


                        </details>


                        <div class="buttons">


                            <a
                                class="btn btn-editar"
                                href="/editar/{{ loop.index0 }}"
                            >

                                ✏️ Editar

                            </a>


                            <a
                                class="btn btn-excluir"
                                href="/delete/{{ loop.index0 }}"
                            >

                                🗑 Excluir

                            </a>


                        </div>


                    </div>


                {% endif %}


            {% endfor %}


        </div>


    </div>


</div>


</body>

</html>
"""


# =============================================================
# Tela de edição
# =============================================================

EDITAR_HTML = """
<!DOCTYPE html>

<html lang="pt-br">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Editar Tarefa</title>


    <style>

        * {
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }


        body {

            min-height: 100vh;

            margin: 0;

            background: linear-gradient(
                135deg,
                #14001f,
                #2d1148,
                #4b1f73,
                #6d28d9
            );

            color: white;

            display: flex;

            justify-content: center;

            align-items: center;

            padding: 40px;
        }


        .container {

            width: 100%;

            max-width: 650px;

            padding: 35px;

            background:
                rgba(255, 255, 255, 0.08);

            border-radius: 28px;
        }


        h1 {

            text-align: center;

            margin-bottom: 30px;
        }


        form {

            display: flex;

            flex-direction: column;

            gap: 15px;
        }


        input,
        select {

            padding: 16px;

            border: none;

            border-radius: 18px;

            background:
                rgba(255, 255, 255, 0.12);

            color: white;

            font-size: 15px;
        }


        select option {

            background: #2d1148;

            color: white;
        }


        button {

            padding: 16px;

            border: none;

            border-radius: 18px;

            background: #2563eb;

            color: white;

            font-weight: bold;

            cursor: pointer;
        }


        .voltar {

            display: block;

            margin-top: 20px;

            text-align: center;

            color: white;

            text-decoration: none;
        }

    </style>

</head>


<body>


<div class="container">


    <h1>

        ✏️ Editar Tarefa

    </h1>


    <form
        method="POST"
        action="/editar/{{ id }}"
    >


        <input
            type="text"
            name="titulo"
            value="{{ tarefa.titulo }}"
            required
        >


        <input
            type="text"
            name="descricao"
            value="{{ tarefa.descricao }}"
            required
        >


        <select
            name="prioridade"
            required
        >


            <option
                value="Alta"
                {% if tarefa.prioridade == "Alta" %}
                    selected
                {% endif %}
            >
                🔴 Alta
            </option>


            <option
                value="Média"
                {% if tarefa.prioridade == "Média" %}
                    selected
                {% endif %}
            >
                🟡 Média
            </option>


            <option
                value="Baixa"
                {% if tarefa.prioridade == "Baixa" %}
                    selected
                {% endif %}
            >
                🟢 Baixa
            </option>


        </select>


        <select
            name="categoria"
            required
        >


            <option
                value="Faculdade"
                {% if tarefa.categoria == "Faculdade" %}
                    selected
                {% endif %}
            >
                🎓 Faculdade
            </option>


            <option
                value="Trabalho"
                {% if tarefa.categoria == "Trabalho" %}
                    selected
                {% endif %}
            >
                💼 Trabalho
            </option>


            <option
                value="Pessoal"
                {% if tarefa.categoria == "Pessoal" %}
                    selected
                {% endif %}
            >
                🏠 Pessoal
            </option>


            <option
                value="Outros"
                {% if tarefa.categoria == "Outros" %}
                    selected
                {% endif %}
            >
                📌 Outros
            </option>


        </select>


        <input
            type="date"
            name="data_limite"
            value="{{ tarefa.data_limite }}"
            required
        >


        <button type="submit">

            💾 Salvar Alterações

        </button>


    </form>


    <a
        href="/"
        class="voltar"
    >

        ← Voltar para o Kanban

    </a>


</div>


</body>

</html>
"""


# =============================================================
# Rotas
# =============================================================


def configure_routes(app) -> None:

    """Registra todos os endpoints do sistema."""


    # ----------------------------------------------------------
    # Página principal
    # ----------------------------------------------------------

    @app.route("/")
    def index():

        return render_template_string(
            HTML,
            tarefas=tarefas
        )


    # ----------------------------------------------------------
    # Adicionar tarefa
    # ----------------------------------------------------------

    @app.route(
        "/add",
        methods=["POST"]
    )
    def add():

        titulo = request.form["titulo"]

        descricao = request.form["descricao"]

        prioridade = request.form["prioridade"]

        categoria = request.form["categoria"]

        data_limite = request.form["data_limite"]


        nova_tarefa = Task(
            titulo,
            descricao,
            prioridade,
            categoria,
            data_limite
        )


        tarefas.append(
            nova_tarefa
        )


        salvar_tarefas()


        return redirect("/")


    # ----------------------------------------------------------
    # Editar tarefa
    # ----------------------------------------------------------

    @app.route(
        "/editar/<int:id>",
        methods=["GET", "POST"]
    )
    def editar(id: int):

        tarefa = tarefas[id]


        if request.method == "POST":


            novo_titulo = request.form["titulo"]

            nova_descricao = request.form["descricao"]

            nova_prioridade = request.form["prioridade"]

            nova_categoria = request.form["categoria"]

            nova_data_limite = request.form["data_limite"]


            # Registra alterações no histórico

            if tarefa.titulo != novo_titulo:

                tarefa.historico.append(
                    f"Título alterado de "
                    f"'{tarefa.titulo}' "
                    f"para '{novo_titulo}'"
                )


            if tarefa.descricao != nova_descricao:

                tarefa.historico.append(
                    "Descrição alterada"
                )


            if tarefa.prioridade != nova_prioridade:

                tarefa.historico.append(
                    f"Prioridade alterada de "
                    f"{tarefa.prioridade} "
                    f"para {nova_prioridade}"
                )


            if tarefa.categoria != nova_categoria:

                tarefa.historico.append(
                    f"Categoria alterada de "
                    f"{tarefa.categoria} "
                    f"para {nova_categoria}"
                )


            if tarefa.data_limite != nova_data_limite:

                tarefa.historico.append(
                    f"Prazo alterado de "
                    f"{tarefa.data_limite} "
                    f"para {nova_data_limite}"
                )


            tarefa.titulo = novo_titulo

            tarefa.descricao = nova_descricao

            tarefa.prioridade = nova_prioridade

            tarefa.categoria = nova_categoria

            tarefa.data_limite = nova_data_limite


            salvar_tarefas()


            return redirect("/")


        return render_template_string(
            EDITAR_HTML,
            tarefa=tarefa,
            id=id
        )


    # ----------------------------------------------------------
    # Iniciar
    # ----------------------------------------------------------

    @app.route(
        "/iniciar/<int:id>"
    )
    def iniciar(id: int):

        tarefas[id].iniciar()

        salvar_tarefas()

        return redirect("/")


    # ----------------------------------------------------------
    # Concluir
    # ----------------------------------------------------------

    @app.route(
        "/concluir/<int:id>"
    )
    def concluir(id: int):

        tarefas[id].concluir()

        salvar_tarefas()

        return redirect("/")


    # ----------------------------------------------------------
    # Excluir
    # ----------------------------------------------------------

    @app.route(
        "/delete/<int:id>"
    )
    def delete(id: int):

        tarefas.pop(id)

        salvar_tarefas()

        return redirect("/")