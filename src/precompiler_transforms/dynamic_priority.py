from transformations import Transform

from srctools import VMF, Entity, conv_int
import logging

LOGGER = logging.getLogger("[Transform][Dynamic Priority]")

@Transform("Dynamic Priority", 10)
def dynamic_priority(vmf: VMF):

    light: Entity

    lights = set(vmf.by_class["light_rt_spot"]) | set(vmf.by_class["light_rt"])

    for light in lights:
        if conv_int(light["_lightmode"], 2) != 2: # Only Baked Bounce makes sense to have this functionality
            continue

        if light["targetname", ""] != "":
            LOGGER.info(f"Lights with targetnames will be skipped! Light: {light['targetname', '']} at {light.get_origin()}")

        dynpr = conv_int(light["_dynamic_priority"], default=-1)
        
        if dynpr not in (0, 1, 2):
            LOGGER.warning(f"Invalid _dynamic_priority for light at {light.get_origin()}, skipping...")
            continue


        if dynpr == 2: # On High, don't change since the light is always dynamic
            continue

        LOGGER.info(f"Processing light at {light.get_origin()}")
        light_copy = light.copy()
        light_bounce = light.copy()

        light_bounce["_lightmode"] = 2 # Ensure Bounce is created
        light_bounce["_removeaftercompile"] = 1 # Make VRAD remove this light after compilation
        # This trick allows us to create artificial bounce-only lights, because named lights don't get bounce lights

        # The thing is, even when switching the modes, bounce lights will remain on, because we're switching between groups and not on/off

        light["targetname"] = f"light_dynpr_dynamic_{dynpr}"
        light_copy["targetname"] = f"light_dynpr_static_{dynpr}"

        # Create a static copy
        light_copy["_lightmode"] = 0 # Fully static

        # We expect the mode to be medium by default, it also limits the amount of lights being switched at once when changing from this mode on map load
        if dynpr == 1: # Medium, set the static light to dark
            spawnflags = conv_int(light_copy["spawnflags", 0])
            spawnflags |= 1 # Sets Initially Dark to True
            light_copy["spawnflags"] = spawnflags
    
        elif dynpr == 0: # Low, set the dynamic light to dark
            spawnflags = conv_int(light["spawnflags", 0])
            spawnflags |= 1 # Sets Initially Dark to True
            light["spawnflags"] = spawnflags

        vmf.add_ents([light_copy, light_bounce])