import ast
import copy
import json
import random
import sys
from typing import Any


class MutantVisitor(ast.NodeTransformer):
    def __init__(self, target_node, mutated_node):
        self.target_node = target_node
        self.mutated_node = mutated_node
        self.mutated = False

    def generic_visit(self, node):
        if node is self.target_node and not self.mutated:
            self.mutated = True
            return self.mutated_node
        return super().generic_visit(node)


def generate_mutants(source: str, max_count: int = 40, seed: int = 42) -> list[dict[str, Any]]:
    random.seed(seed)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    lines = source.splitlines()
    mutants = []
    mutant_id = 1

    candidates = []

    # Operators mapping
    cmp_ops = {
        ast.Eq: ast.NotEq,
        ast.NotEq: ast.Eq,
        ast.Lt: ast.Gt,
        ast.LtE: ast.GtE,
        ast.Gt: ast.Lt,
        ast.GtE: ast.LtE,
    }
    arith_ops = {
        ast.Add: ast.Sub,
        ast.Sub: ast.Add,
        ast.Mult: ast.Div,
        ast.Div: ast.Mult,
        ast.FloorDiv: ast.Mult,
    }
    bool_ops = {ast.And: ast.Or, ast.Or: ast.And}

    for node in ast.walk(tree):
        if not hasattr(node, "lineno"):
            continue

        if isinstance(node, ast.Compare):
            for i, op in enumerate(node.ops):
                if type(op) in cmp_ops:
                    new_node = copy.deepcopy(node)
                    new_node.ops[i] = cmp_ops[type(op)]()
                    candidates.append(("comparison_swap", node, new_node))

        elif isinstance(node, ast.BinOp):
            if type(node.op) in arith_ops:
                new_node = copy.deepcopy(node)
                new_node.op = arith_ops[type(node.op)]()
                candidates.append(("arithmetic_swap", node, new_node))

        elif isinstance(node, ast.BoolOp):
            if type(node.op) in bool_ops:
                new_node = copy.deepcopy(node)
                new_node.op = bool_ops[type(node.op)]()
                candidates.append(("boolean_swap", node, new_node))

        elif isinstance(node, ast.Constant):
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                new_node = copy.deepcopy(node)
                new_node.value = node.value + 1
                candidates.append(("constant_shift", node, new_node))

    random.shuffle(candidates)
    candidates = candidates[:max_count]

    for op_name, orig_node, new_node in candidates:
        mutated_tree = copy.deepcopy(tree)
        MutantVisitor(orig_node, new_node)
        # We need a proper way to replace the specific node instance in the copied tree
        # For simplicity in this demo tool, we will use ast.unparse which is available in 3.9+

        # A more robust approach requires matching node locations
        class ReplaceByLoc(ast.NodeTransformer):
            def __init__(self, target, replacement):
                self.target = target
                self.replacement = replacement
                self.done = False

            def generic_visit(self, n):
                if not self.done and hasattr(n, "lineno") and hasattr(n, "col_offset"):
                    if (
                        n.lineno == self.target.lineno
                        and n.col_offset == self.target.col_offset
                        and type(n) == type(self.target)
                    ):
                        self.done = True
                        return self.replacement
                return super().generic_visit(n)

        replacer = ReplaceByLoc(orig_node, new_node)
        mutated_tree = replacer.visit(mutated_tree)
        ast.fix_missing_locations(mutated_tree)

        try:
            mutated_source = ast.unparse(mutated_tree)
            if mutated_source != source:
                mutants.append(
                    {
                        "id": mutant_id,
                        "operator": op_name,
                        "function_name": "unknown",  # simplified
                        "line": orig_node.lineno,
                        "original": lines[orig_node.lineno - 1]
                        if orig_node.lineno <= len(lines)
                        else "",
                        "mutated": mutated_source.splitlines()[orig_node.lineno - 1]
                        if orig_node.lineno <= len(mutated_source.splitlines())
                        else "",
                        "full_source": mutated_source,
                    }
                )
                mutant_id += 1
        except Exception:
            pass

    return mutants


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print(json.dumps(generate_mutants(f.read()), indent=2))
