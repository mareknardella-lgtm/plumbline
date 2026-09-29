import ast
import json
import sys
from typing import Any

EFFECTS = {
    "print": ["print"],
    "time": ["time", "sleep", "datetime", "utcnow"],
    "random": ["random", "randint", "choice", "shuffle", "seed"],
    "network": ["requests", "urllib", "socket", "urlopen", "HTTPConnection"],
    "io": ["open", "read", "write", "FileIO", "TextIOWrapper"],
    "env": ["os", "sys", "environ", "getenv"],
    "globals": ["global"],
}


class SurveyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = set()
        self.effects = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append(
            {
                "name": node.name,
                "signature": self._get_signature(node),
                "docstring": ast.get_docstring(node),
                "line": node.lineno,
                "is_public": not node.name.startswith("_"),
                "effects": [],
            }
        )
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        self.classes.append({"name": node.name, "methods": methods, "line": node.lineno})
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self._check_effects(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self._check_effects(node.func.attr)
        self.generic_visit(node)

    def visit_Global(self, node):
        self.effects.add("globals")
        self.generic_visit(node)

    def _get_signature(self, node):
        args = [arg.arg for arg in node.args.args]
        return f"({', '.join(args)})"

    def _check_effects(self, name):
        for effect_type, indicators in EFFECTS.items():
            if name in indicators:
                self.effects.add(effect_type)


def survey_source(source_code: str) -> dict[str, Any]:
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"error": str(e)}

    visitor = SurveyVisitor()
    visitor.visit(tree)

    return {
        "functions": visitor.functions,
        "classes": visitor.classes,
        "imports": list(visitor.imports),
        "module_docstring": ast.get_docstring(tree),
        "lines_of_code": len(source_code.splitlines()),
        "effects_summary": list(visitor.effects),
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print(json.dumps(survey_source(f.read()), indent=2))
