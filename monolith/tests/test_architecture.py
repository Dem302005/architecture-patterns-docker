import ast
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "app"


def imports_of(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names.append(node.module or "")
    return names


def layer_files(layer):
    return list((ROOT / layer).rglob("*.py"))


def test_presentation_does_not_import_infrastructure():
    for path in layer_files("presentation"):
        assert not [n for n in imports_of(path) if "infrastructure" in n], path


def test_application_depends_only_on_domain():
    for path in layer_files("application"):
        bad = [n for n in imports_of(path) if "infrastructure" in n or "presentation" in n]
        assert not bad, path


def test_domain_is_independent():
    for path in layer_files("domain"):
        bad = [n for n in imports_of(path) if n.startswith("app.") and not n.startswith("app.domain")]
        assert not bad, path
