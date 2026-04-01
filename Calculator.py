import ast
import operator as op
import tkinter as tk
from tkinter import ttk


_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _safe_eval(expr: str) -> float:
    """
    Evaluate a simple arithmetic expression safely.
    Allowed: numbers, +, -, *, /, unary +/-, and parentheses.
    """

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Invalid expression")

    tree = ast.parse(expr, mode="eval")
    return float(_eval(tree))


class CalculatorApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=16)
        self.master = master
        self._expr = tk.StringVar(value="")
        self._status = tk.StringVar(value="Ready")

        self._build_styles()
        self._build_ui()
        self._bind_keys()

    def _build_styles(self):
        self.master.title("PythonCalc")
        self.master.minsize(360, 520)
        self.master.configure(background="#0b1220")

        style = ttk.Style(self.master)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background="#0b1220")
        style.configure(
            "Display.TEntry",
            fieldbackground="#0f1a2e",
            background="#0f1a2e",
            foreground="#e6eefc",
            insertcolor="#e6eefc",
            bordercolor="#223052",
            relief="flat",
            padding=(12, 14),
            font=("Segoe UI", 22),
        )
        style.configure(
            "Status.TLabel",
            background="#0b1220",
            foreground="#9bb0d6",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Btn.TButton",
            padding=(10, 10),
            font=("Segoe UI", 12),
            background="#122242",
            foreground="#e6eefc",
            borderwidth=0,
            focusthickness=1,
            focuscolor="#3b82f6",
        )
        style.map(
            "Btn.TButton",
            background=[("active", "#17305b"), ("pressed", "#0e1b35")],
            foreground=[("disabled", "#6b7ca0")],
        )
        style.configure(
            "Op.TButton",
            padding=(10, 10),
            font=("Segoe UI", 12, "bold"),
            background="#1f3a72",
            foreground="#e6eefc",
            borderwidth=0,
        )
        style.map(
            "Op.TButton",
            background=[("active", "#2a4a8f"), ("pressed", "#14274c")],
        )
        style.configure(
            "Eq.TButton",
            padding=(10, 12),
            font=("Segoe UI", 12, "bold"),
            background="#2563eb",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Eq.TButton",
            background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
        )
        style.configure(
            "Danger.TButton",
            padding=(10, 10),
            font=("Segoe UI", 12, "bold"),
            background="#7f1d1d",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#991b1b"), ("pressed", "#5f1717")],
        )

    def _build_ui(self):
        self.configure(style="App.TFrame")
        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        display = ttk.Entry(
            self,
            textvariable=self._expr,
            justify="right",
            style="Display.TEntry",
        )
        display.grid(row=0, column=0, sticky="ew")
        display.focus_set()

        status = ttk.Label(self, textvariable=self._status, style="Status.TLabel")
        status.grid(row=1, column=0, sticky="w", pady=(10, 12))

        pad = ttk.Frame(self, style="App.TFrame")
        pad.grid(row=2, column=0, sticky="nsew")
        for c in range(4):
            pad.columnconfigure(c, weight=1, uniform="col")
        for r in range(5):
            pad.rowconfigure(r, weight=1, uniform="row")

        def b(text, r, c, *, style="Btn.TButton", colspan=1, cmd=None):
            btn = ttk.Button(
                pad,
                text=text,
                style=style,
                command=cmd or (lambda t=text: self._press(t)),
            )
            btn.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=6, pady=6)
            return btn

        b("C", 0, 0, style="Danger.TButton", cmd=self._clear)
        b("⌫", 0, 1, style="Btn.TButton", cmd=self._backspace)
        b("(", 0, 2, style="Btn.TButton")
        b(")", 0, 3, style="Btn.TButton")

        b("7", 1, 0)
        b("8", 1, 1)
        b("9", 1, 2)
        b("÷", 1, 3, style="Op.TButton", cmd=lambda: self._press("/"))

        b("4", 2, 0)
        b("5", 2, 1)
        b("6", 2, 2)
        b("×", 2, 3, style="Op.TButton", cmd=lambda: self._press("*"))

        b("1", 3, 0)
        b("2", 3, 1)
        b("3", 3, 2)
        b("−", 3, 3, style="Op.TButton", cmd=lambda: self._press("-"))

        b("0", 4, 0, colspan=2)
        b(".", 4, 2, cmd=self._press_decimal)
        b("+", 4, 3, style="Op.TButton", cmd=lambda: self._press("+"))

        eq = ttk.Button(pad, text="=", style="Eq.TButton", command=self._equals)
        eq.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=6, pady=(10, 0))
        pad.rowconfigure(5, weight=1, uniform="row")

    def _bind_keys(self):
        def on_key(event: tk.Event):
            ch = event.char
            if ch in "0123456789()+-*/":
                self._press(ch)
                return "break"
            if ch == ".":
                self._press_decimal()
                return "break"
            if event.keysym in ("Return", "KP_Enter"):
                self._equals()
                return "break"
            if event.keysym in ("BackSpace",):
                self._backspace()
                return "break"
            if event.keysym in ("Escape",):
                self._clear()
                return "break"
            return None

        self.master.bind("<Key>", on_key)

    def _set_status(self, msg: str):
        self._status.set(msg)

    def _press(self, token: str):
        self._expr.set(self._expr.get() + token)
        self._set_status("Ready")

    def _press_decimal(self):
        expr = self._expr.get()
        i = max(expr.rfind("+"), expr.rfind("-"), expr.rfind("*"), expr.rfind("/"), expr.rfind("("))
        current = expr[i + 1 :]
        if "." in current:
            return
        if current == "":
            self._expr.set(expr + "0.")
        else:
            self._expr.set(expr + ".")
        self._set_status("Ready")

    def _clear(self):
        self._expr.set("")
        self._set_status("Cleared")

    def _backspace(self):
        s = self._expr.get()
        if s:
            self._expr.set(s[:-1])
        self._set_status("Ready")

    def _equals(self):
        expr = self._expr.get().strip()
        if not expr:
            self._set_status("Ready")
            return

        try:
            result = _safe_eval(expr)
            if result.is_integer():
                out = str(int(result))
            else:
                out = f"{result:.12g}"
            self._expr.set(out)
            self._set_status("OK")
        except ZeroDivisionError:
            self._set_status("Error: divide by zero")
        except Exception:
            self._set_status("Error: invalid expression")


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


