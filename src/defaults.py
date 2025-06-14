HELP_MSG = """
Tool used to make transformations on the vmf file itself; that need to be done before VBSP runs.

Usage: call like you would call VBSP, this tool will handle the transformations and then launch VBSP from within itself.
You can even replace the VBSP path with the path to this exe, however make sure to provide the vbsp path in the precompiler_cfg.vdf file.

Special options:

-h 
Write this message

-write_cfg_default
Writes the default precompiler_cfg.vdf file next to the executable. Use if the config has been corrupted somehow and needs to be reset.

-no-remove
Doesn't remove the <map_name>_precompiled.vmf file after processing."""




DEFAULT_CFG = '''"Config" {
    // Main folder name, where all your mod assets are stored in.
    // For example for P2CE it's "Portal 2 Community Edition"
    // This will set the base path of all the paths below to .../Portal-Singularity-Collapse/
    // The folder name here will get searched through all parents of the map path specified when invoking precompiler.
    "prefix_path" ""

    // Location of the VBSP executable
    "vbsp_path" "you_have_to_set_this_manually_in_precompiler_cfg.vdf"

    // Location of the transforms folder
    "transforms_loc" "precompiler_transforms/" 
}
'''