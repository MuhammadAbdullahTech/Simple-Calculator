import ast
import operator as op

# Calculator.py
# Simple safe calculator that evaluates arithmetic expressions using Python's ast.
# Usage: run and type expressions like: 2+3*4, (1+2)/3, -5**2, 2**10, 10%3
# Type "quit" or "q" to exit.


# supported operators
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    if isinstance(node, ast.Num):  # for older ASTs
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            func = _OPERATORS[op_type]
            return func(left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            func = _OPERATORS[op_type]
            return func(operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")
    raise ValueError(f"Unsupported expression: {type(node).__name__}")

def safe_eval(expr):
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e
    return _eval(parsed)

def main():
    # Try to launch a simple Tkinter GUI. If Tkinter isn't available or GUI can't start,
    # fall back to the original command-line interface.
    try:
        import tkinter as tk
        from tkinter import ttk

        def format_result(res):
            if isinstance(res, float) and res.is_integer():
                return str(int(res))
            return str(res)

        root = tk.Tk()
        root.title("Simple Calculator")
        root.resizable(False, False)

        style = ttk.Style()
        style.configure("TButton", padding=6)

        entry = ttk.Entry(root, font=(None, 16), justify="right")
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        def insert(char):
            entry.insert(tk.END, char)

        def clear():
            entry.delete(0, tk.END)

        def backspace():
            s = entry.get()
            if s:
                entry.delete(len(s)-1, tk.END)

        def evaluate(event=None):
            expr = entry.get().replace('^', '**')
            try:
                res = safe_eval(expr)
                entry.delete(0, tk.END)
                entry.insert(0, format_result(res))
            except Exception as e:
                entry.delete(0, tk.END)
                entry.insert(0, "Error")

        btn_texts = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('%', 4, 2), ('+', 4, 3),
        ]

        for (txt, r, c) in btn_texts:
            b = ttk.Button(root, text=txt, command=lambda t=txt: insert(t))
            b.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        eq = ttk.Button(root, text='=', command=evaluate)
        eq.grid(row=5, column=3, sticky="nsew", padx=2, pady=2)

        clear_btn = ttk.Button(root, text='C', command=clear)
        clear_btn.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)

        back_btn = ttk.Button(root, text='⌫', command=backspace)
        back_btn.grid(row=5, column=1, sticky="nsew", padx=2, pady=2)

        pow_btn = ttk.Button(root, text='^', command=lambda: insert('^'))
        pow_btn.grid(row=5, column=2, sticky="nsew", padx=2, pady=2)

        # make columns expand evenly
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

        # key bindings
        entry.bind('<Return>', evaluate)
        entry.bind('<BackSpace>', lambda e: None)  # default works on entry

        # set initial focus
        entry.focus()

        root.mainloop()

    except Exception:
        # Fallback to CLI if GUI can't start
        print("Simple Calculator. Enter arithmetic expressions. Type 'q' or 'quit' to exit.")
        while True:
            try:
                s = input("» ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not s:
                continue
            if s.lower() in {"q", "quit", "exit"}:
                break
            try:
                result = safe_eval(s)
                # Print integers without decimal point
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                print(result)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()