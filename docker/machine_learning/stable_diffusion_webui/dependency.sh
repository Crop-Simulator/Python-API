#!/bin/bash

set -Eeuo pipefail

# Install all the dependencies for the extensions
shopt -s nullglob
# For install.py, please refer to https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions#installpy
list=(${ROOT}/extensions/*/install.py)
for installscript in "${list[@]}"; do
  echo Running ${installscript}
  PYTHONPATH=${ROOT} python "$installscript"
done
