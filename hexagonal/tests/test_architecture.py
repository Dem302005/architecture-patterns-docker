import ast
import pathlib

CORE = pathlib.Path(__file__).resolve().parent.parent / "core"


def test_core_does_not_import_adapters_or_config():
    for path in CORE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                assert not name.startswith(("adapters", "config", "flask", "psycopg2")), (path, name)
