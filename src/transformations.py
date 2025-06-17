"""Handles the transformations"""

from srctools import VMF
from pathlib import Path
import importlib
import logging
import pkgutil

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




def load_transforms(transforms_path: Path):
    for item in pkgutil.iter_modules([transforms_path]):
        importlib.import_module(transforms_path.name + "." + item.name)

def run_transforms(vmf_file: VMF):
    for priority in sorted(TRANSFORMATIONS.keys())[::-1]:
        for name, func in TRANSFORMATIONS[priority]:
            LOGGER.info(f"Running transform |{name}|")
            func(vmf_file)
    