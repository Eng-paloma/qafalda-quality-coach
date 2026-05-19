from .app import QAfalda


def run_cli() -> None:
    bot = QAfalda()
    print("QAfalda — Coach de Qualidade de Teste")
    print("Digite 'sair' para encerrar.")
    while True:
        question = input("Você: ").strip()
        if not question:
            continue
        if question.lower() in {"sair", "exit", "quit"}:
            print("QAfalda: Até logo! Continue estudando qualidade.")
            break
        answer = bot.respond(question)
        print(f"QAfalda: {answer}\n")
