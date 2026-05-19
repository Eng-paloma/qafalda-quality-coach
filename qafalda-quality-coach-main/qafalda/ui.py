import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from .app import QAfalda

WINDOW_BG = "#f7f3ef"
HEADER_BG = "#3c5866"
HEADER_FG = "#f4f1e9"
BUBBLE_BG = "#ffffff"
USER_BG = "#d1e7f0"
BOT_BG = "#f3e5ab"
BUTTON_BG = "#5c6c79"


class QAfaldaApp:
    def __init__(self, root: tk.Tk):
        self.bot = QAfalda()
        self.root = root
        self.root.title("QAfalda — Coach de Qualidade")
        self.root.geometry("720x540")
        self.root.configure(bg=WINDOW_BG)
        self._build_interface()
        self._greet()

    def _build_interface(self) -> None:
        header = tk.Frame(self.root, bg=HEADER_BG, height=110)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="QAfalda",
            bg=HEADER_BG,
            fg=HEADER_FG,
            font=("Helvetica", 28, "bold"),
        )
        title.pack(anchor="w", padx=24, pady=(18, 4))

        subtitle = tk.Label(
            header,
            text="Seu coach minimalista de qualidade de teste",
            bg=HEADER_BG,
            fg=HEADER_FG,
            font=("Helvetica", 12),
        )
        subtitle.pack(anchor="w", padx=24)

        self.chat_frame = tk.Frame(self.root, bg=WINDOW_BG)
        self.chat_frame.pack(fill="both", expand=True, padx=18, pady=12)

        self.chat_box = ScrolledText(
            self.chat_frame,
            wrap="word",
            state="disabled",
            bg=BUBBLE_BG,
            fg="#242424",
            font=("Segoe UI", 11),
            bd=0,
            padx=12,
            pady=12,
            relief="flat",
            highlightthickness=0,
        )
        self.chat_box.pack(fill="both", expand=True, pady=(0, 10))

        input_frame = tk.Frame(self.root, bg=WINDOW_BG)
        input_frame.pack(fill="x", padx=18, pady=(0, 18))

        self.user_entry = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.user_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 12))
        self.user_entry.bind("<Return>", self._handle_submit)

        send_button = tk.Button(
            input_frame,
            text="Enviar",
            command=self._handle_submit,
            bg=BUTTON_BG,
            fg="white",
            activebackground="#3f505a",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=8,
        )
        send_button.pack(side="right")

    def _greet(self) -> None:
        greeting = (
            "Bem-vindo ao QAfalda! \n" "Pergunte qualquer coisa sobre qualidade de teste, BSQTB-CTFL 4.0 e práticas de auditoria."
        )
        self._append_message("QAfalda", greeting)

    def _append_message(self, sender: str, message: str) -> None:
        self.chat_box.configure(state="normal")
        if sender == "QAfalda":
            self.chat_box.insert("end", f"QAfalda:\n", "bot_tag")
            self.chat_box.insert("end", f"{message}\n\n")
        else:
            self.chat_box.insert("end", f"Você:\n", "user_tag")
            self.chat_box.insert("end", f"{message}\n\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.yview("end")

    def _handle_submit(self, event=None) -> None:
        question = self.user_entry.get().strip()
        if not question:
            return
        self.user_entry.delete(0, "end")
        self._append_message("Você", question)
        answer = self.bot.respond(question)
        self._append_message("QAfalda", answer)


def run_app() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    app = QAfaldaApp(root)
    root.mainloop()
