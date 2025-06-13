from sys import argv, stdout
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from transformations import run_transforms

from srctools import Keyvalues

from defaults import HELP_MSG, DEFAULT_CFG

OUR_PATH = Path(argv[0]).parent

LOGGER = logging.getLogger("[Main]")
handlers = [logging.StreamHandler(stdout), RotatingFileHandler(OUR_PATH.joinpath("precompiler.log"), mode="w", backupCount=5)]
logging.basicConfig(handlers=handlers, level=logging.INFO)





def main():

    LOGGER.info("Running precompiler!")

    if "-h" in argv:
        LOGGER.info("Printing help message...")
        LOGGER.info(HELP_MSG)

    if "-write_cfg_default":
        LOGGER.info("Called write config default!")
        dst_path = OUR_PATH.joinpath("precompiler_cfg.vdf")
        LOGGER.info(f"Writing into {dst_path}")
        with open(dst_path, "w") as cfg_file:
            cfg_file.write(DEFAULT_CFG)

        exit(0)

    if len(argv) < 4:
        LOGGER.error("Invalid argument count, at least 3 are needed (-game $gamedir map)!")
        raise RuntimeError


    # Map path handling
    map_path = Path(argv[-1])
    map_path = map_path.with_suffix(".vmf")
    
    if not map_path.is_file():
        LOGGER.error(f"Invalid map path {map_path}!")
        raise FileNotFoundError
    
    LOGGER.info(f"Map path is: {map_path}")


    # Store vbsp args for later use
    vbsp_args = argv[1:-1] # First is our path, last is the map path which will be different either way
    LOGGER.info(f"VBSP args are: {vbsp_args}")


    
    # Locate and load the config file
    for p in [OUR_PATH] + OUR_PATH.parents:
        try_path: Path = p.joinpath("precompiler_cfg.vdf")

        if try_path.is_file():
            with open(try_path, 'r') as cfg_file:
                cfg = Keyvalues.parse(cfg_file.read())

    


    run_transforms(OUR_PATH.joinpath("precompiler_transforms"), "")
    


if __name__ == "__main__":
    main()