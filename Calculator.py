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