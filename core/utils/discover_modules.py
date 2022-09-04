import importlib
from pathlib import Path


def discover_modules(path: str):
    currect_path = Path('.')

    model_pathes = map(lambda module_path: str(module_path).replace('/', '.'), currect_path.glob(path))
    for path in model_pathes:
        importlib.import_module(path)
