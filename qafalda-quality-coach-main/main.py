import os

from qafalda.cli import run_cli
from qafalda.ui import run_app


def main() -> None:
    if os.environ.get("DISPLAY"):
        try:
            run_app()
            return
        except Exception as exc:
            print("Não foi possível abrir a interface gráfica:", exc)

    print("Ambiente sem DISPLAY ou interface gráfica indisponível. Usando modo texto.")
    run_cli()


if __name__ == "__main__":
    main()
