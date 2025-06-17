#!/bin/bash

python -m nuitka --assume-yes-for-downloads --mode=onefile --output-dir=build src/precompiler.py

for i in src/precompiler_transforms/*.py; do
    python -m nuitka --assume-yes-for-downloads --mode=module --output-dir=build $i
done

mkdir dist
mkdir dist/precompiler_transforms

for i in build/*.pyd; do
    cp $i dist/precompiler_transforms
done

if [ "$RUNNER_OS" == "Linux" ]; then
    chmod +x build/precompiler.bin
    build/precompiler.bin -write_cfg_default
    cp build/precompiler.bin dist/
    cp build/precompiler_cfg.vdf dist/

elif [ "$RUNNER_OS" == "Windows" ]; then
    build/precompiler.exe -write_cfg_default
    cp build/precompiler.exe dist/
    cp build/precompiler_cfg.vdf dist/
else
    echo "$RUNNER_OS not supported"
    exit 1
fi


