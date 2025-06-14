"""Handles the transformations"""

from srctools import VMF
from pathlib import Path
import importlib.util
import sys
import logging


TRANSFORMATIONS: dict[int, list] = {}
LOGGER = logging.getLogger("[Transformations]")

def Transform(name: str, priority:int = 0):
    """Add a function to the transformations list"""

    def dec(func):
        func = (name, func)
        global TRANSFORMATIONS
        try:
            l = TRANSFORMATIONS[priority]
            l.append(func)
        except KeyError:
            TRANSFORMATIONS[priority] = [func]
        
        return func

    LOGGER.info(f"Loading module '{name}'")

    return dec

    

# "Borrowed" from the importlib wiki
def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_transforms(transforms_path: Path):
    for _file in transforms_path.rglob("*.py"):
        import_from_path(_file.stem, _file)

def run_transforms(vmf_file: VMF):
    for priority in sorted(TRANSFORMATIONS.keys())[::-1]:
        for name, func in TRANSFORMATIONS[priority]:
            LOGGER.info(f"Running transform |{name}|")
            func(vmf_file)
    