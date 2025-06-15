from sys import argv, stdout, exit
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from transformations import run_transforms, load_transforms

from srctools import Keyvalues, VMF, run

from defaults import HELP_MSG, DEFAULT_CFG

from os import remove, rename

OUR_PATH = Path(argv[0]).parent

LOGGER = logging.getLogger("[Main]")
handlers = [logging.StreamHandler(stdout), RotatingFileHandler(OUR_PATH.joinpath("precompiler.log"), mode="w", backupCount=5)]
logging.basicConfig(handlers=handlers, level=logging.INFO)


PATHS: dict[str, Path] = {}

MAP_VMF = None

def main():

    global MAP_VMF, PATHS

    LOGGER.info("Running precompiler!")

    if "-h" in argv:
        LOGGER.info("Printing help message...")
        LOGGER.info(HELP_MSG)

    if "-write_cfg_default" in argv:
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
    PATHS["map_path"] = Path(argv[-1])
    PATHS["map_path"] = PATHS["map_path"].with_suffix(".vmf")
    
    if not PATHS["map_path"].is_file():
        LOGGER.error(f"Invalid map path {PATHS["map_path"]}!")
        raise FileNotFoundError
    
    LOGGER.info(f"Map path is: {PATHS["map_path"]}")


    # Store vbsp args for later use
    vbsp_args = argv[1:-1] # First is our path, last is the map path which will be different either way
    LOGGER.info(f"VBSP args are: {vbsp_args}")


    cfg = None
    # Locate and load the config file
    for p in [OUR_PATH] + list(OUR_PATH.parents):
        try_path: Path = p.joinpath("precompiler_cfg.vdf")

        if try_path.is_file():
            LOGGER.info(f"Loading config from {try_path}")
            with open(try_path, 'r') as cfg_file:
                cfg = Keyvalues.parse(cfg_file.read())
                cfg = cfg.find_block("Config")
            break

    if cfg is None:
        LOGGER.error("Couldn't find any cfg file!")
        raise FileNotFoundError


    PATHS["prefix_path"] = None
    # Locate the prefix path
    for p in [PATHS["map_path"]] + list(PATHS["map_path"].parents):
        if p.stem.casefold() == cfg["prefix_path"].casefold():
            PATHS["prefix_path"] = p
            break

    if PATHS["prefix_path"] is None:
        LOGGER.error("Couldn't find the prefix path specified!")
        raise FileNotFoundError
    
    
    LOGGER.info(f"Prefix path is: {PATHS['prefix_path']}")

    PATHS["vbsp"] = PATHS["prefix_path"].joinpath(cfg["vbsp_path"])
    if not PATHS["vbsp"].is_file():
        LOGGER.error(f"Cannot find VBSP executable at {PATHS['vbsp']}")
        raise FileNotFoundError
    
    LOGGER.info(f"VBSP path is: {PATHS['vbsp']}")
    


    PATHS["transforms"] = PATHS["prefix_path"].joinpath(cfg["transforms_loc"])
    if not PATHS["transforms"].is_dir():
        LOGGER.error(f"Specified path for transforms is invalid: {PATHS['transforms']}")
        raise FileNotFoundError
    
    LOGGER.info(f"Loading transforms from {PATHS['transforms']}")

    load_transforms(PATHS["transforms"])

    LOGGER.info("Success!")
    LOGGER.info("Loading map...")


    with open(PATHS["map_path"], "r") as map_file:
        MAP_VMF = Keyvalues.parse(map_file.read())
    
    MAP_VMF = VMF.parse(MAP_VMF)



    LOGGER.info("Loaded! Running transforms...")
    run_transforms(MAP_VMF)
    LOGGER.info("Transforms complete!")

    LOGGER.info("Saving and proceeding to run VBSP...")

    map_name = PATHS["map_path"].stem
    new_path = PATHS["map_path"].parent.joinpath(f"{map_name}_precompiled.vmf")

    with open(new_path, "w") as map_file:
        MAP_VMF.export(map_file, inc_version=False)

    LOGGER.info("_____VBSP_____")

    vbsp_args += [new_path.as_posix()]
    LOGGER.debug(f"VBSP args: {[PATHS['vbsp'].__str__()] + vbsp_args }")
    # Start the vbsp compilation process
    run.run_compiler(
        name=PATHS['vbsp'],
        args=vbsp_args,
        change_name=False
    )

    LOGGER.info("Done! Cleaning up...")

    if not "-no-remove" in argv:
        remove(new_path)

    for file_ in new_path.parent.rglob(f"{map_name}_precompiled.*"):
        rename(file_, file_.parent.joinpath(f"{map_name}"+file_.suffix))

    LOGGER.info("Finished.")
    


    


    


if __name__ == "__main__":
    main()
