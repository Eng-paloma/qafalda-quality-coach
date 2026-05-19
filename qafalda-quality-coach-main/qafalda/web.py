import os
import random
from math import ceil
from flask import Flask, render_template, request
from .knowledge import KNOWLEDGE

CTFL_SUGGESTIONS = [
    "Fundamentos do teste",
    "Teste ao longo do ciclo de vida",
    "Teste estático",
    "Análise e projeto de testes",
    "Gerenciamento das atividades de teste",
    "Ferramentas de teste",
]

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)
app.secret_key = 'qafalda-secret-key-2024'


def build_study_plan(selected_topics: list[str], weeks: int, hours_per_week: int, level: str) -> list[dict]:
    topics = selected_topics if selected_topics else CTFL_SUGGESTIONS
    topics_per_week = max(1, ceil(len(topics) / max(weeks, 1)))
    plan = []

    for week in range(1, weeks + 1):
        start = (week - 1) * topics_per_week
        end = start + topics_per_week
        week_topics = topics[start:end]
        if not week_topics:
            week_topics = ["Revisão geral CTFL"]

        if level == "iniciante":
            foco = "foco em conceitos-base e exemplos simples"
        elif level == "intermediario":
            foco = "foco em aplicação prática e comparação de técnicas"
        else:
            foco = "foco em cenários reais, risco e decisão de cobertura"

        atividades = [
            f"Estudar: {', '.join(week_topics)}",
            f"Resolver 10 questões sobre os temas da semana ({foco})",
            "Fazer revisão ativa com resumo de 1 página",
        ]

        if hours_per_week >= 6:
            atividades.append("Reservar 1 sessão extra para simulado curto e análise de erros")

        plan.append(
            {
                "week": week,
                "topics": week_topics,
                "hours": hours_per_week,
                "activities": atividades,
            }
        )

    return plan


@app.route("/", methods=["GET", "POST"])
def index():
    plan = None
    form = {
        "weeks": 6,
        "hours_per_week": 5,
        "level": "iniciante",
        "topics": CTFL_SUGGESTIONS,
    }

    if request.method == "POST":
        weeks = max(2, min(16, int(request.form.get("weeks", 6))))
        hours_per_week = max(2, min(20, int(request.form.get("hours_per_week", 5))))
        level = request.form.get("level", "iniciante")
        topics = request.form.getlist("topics")
        valid_topics = [t for t in topics if t in CTFL_SUGGESTIONS]

        form = {
            "weeks": weeks,
            "hours_per_week": hours_per_week,
            "level": level,
            "topics": valid_topics if valid_topics else CTFL_SUGGESTIONS,
        }
        plan = build_study_plan(form["topics"], weeks, hours_per_week, level)

    return render_template(
        "index.html",
        plan=plan,
        form=form,
        suggestions=CTFL_SUGGESTIONS,
    )


@app.route("/temas")
def temas():
    return render_template("temas.html", knowledge=KNOWLEDGE)


@app.route("/dicas")
def dicas():
    dica = random.choice(KNOWLEDGE)
    return render_template("dicas.html", dica=dica)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        selected = request.form.get("answer")
        correct = request.form.get("correct")
        question = request.form.get("question")
        feedback = "Correto! Parabéns." if selected == correct else f"Incorreto. A resposta certa é: {correct}"
        return render_template("quiz.html", feedback=feedback, question=question)

    # Generate quiz question
    item = random.choice(KNOWLEDGE)
    question = item["question"]
    correct_answer = item["answer"]
    options = [correct_answer]

    # Add 3 wrong options from other items
    other_answers = [k["answer"] for k in KNOWLEDGE if k != item]
    options.extend(random.sample(other_answers, min(3, len(other_answers))))
    random.shuffle(options)

    return render_template("quiz.html", question=question, options=options, correct=correct_answer)


def run_web() -> None:
    app.run(host="0.0.0.0", port=5000)
