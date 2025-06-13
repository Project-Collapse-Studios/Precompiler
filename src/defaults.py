HELP_MSG = """
Tool used to make transformations on the vmf file itself; that need to be done before VBSP runs.

Usage: call like you would call VBSP, this tool will handle the transformations and then launch VBSP from within itself.
You can even replace the VBSP path with the path to this exe, however make sure to provide the vbsp path in the precompiler_cfg.vdf file.

Special options:

-h 
Write this message

-write_cfg_default
Writes the default precompiler_cfg.vdf file next to the executable. Use if the config has been corrupted somehow and needs to be reset."""




DEFAULT_CFG = '''"Config" {
    // Prefix path, the base path which every path below inherits from. Relative to the executable of the precompiler
    "prefix_path" ""

    // Location of the VBSP executable
    "vbsp_path" "you_have_to_set_this_manually_in_precompiler_cfg.vdf"

    // Location of the transforms folder
    "transforms_loc" "precompiler_transforms/" 
}
'''