import ast
import math
import operator


_ALLOWED = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Only numeric arithmetic expressions are allowed")


def calculate(expression: str) -> float:
    """Evaluate a bounded numeric expression without executing arbitrary code."""
    if len(expression) > 200:
        raise ValueError("Expression is too long")
    tree = ast.parse(expression, mode="eval")
    value = _eval(tree.body)
    if not math.isfinite(value):
        raise ValueError("Result is not finite")
    return round(value, 8)


CALCULATOR_DECLARATION = {
    "name": "calculate",
    "description": "Perform exact arithmetic for unit economics, percentages, ratios, ICE scores, and experiment calculations.",
    "parameters": {
        "type": "object",
        "properties": {"expression": {"type": "string"}},
        "required": ["expression"],
    },
}
