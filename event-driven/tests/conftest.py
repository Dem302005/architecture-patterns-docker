import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
for name in ("orders", "billing", "notifications"):
    sys.path.insert(0, str(ROOT / "services" / name))
