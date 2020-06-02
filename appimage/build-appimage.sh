#!/usr/bin/env bash

version=0.4.0

mkdir -p build && cd build

wget -nc "https://raw.githubusercontent.com/TheAssassin/linuxdeploy-plugin-conda/master/linuxdeploy-plugin-conda.sh"
wget -nc "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
chmod +x linuxdeploy-x86_64.AppImage linuxdeploy-plugin-conda.sh
cp ../appimage/AppRun.sh .

cat > spr.desktop <<EOF
[Desktop Entry]
Type=Application
Name=spr
GenericName=Spice Raw Parser
Comment=Spice Raw Parser -- a CLI tool to parse and plot spice raw data files.
Icon=spr
Exec=spr
Terminal=true
Categories=Utility;
EOF

export PKG_OUT_DIR=pkg-out

mkdir -p $PKG_OUT_DIR
conda build --output-folder $PKG_OUT_DIR ..

export CONDA_PYTHON_VERSION="3.6"
export CONDA_CHANNELS="conda-forge"
export CONDA_PACKAGES=$PKG_OUT_DIR/linux-64/spr-$version-py36_0.tar.bz2
export PIP_REQUIREMENTS='numpy matplotlib tabulate'

./linuxdeploy-x86_64.AppImage \
    --appdir AppDir \
    -i ../appimage/spr.png \
    -d spr.desktop \
    --plugin conda \
    --custom-apprun AppRun.sh \
    --output appimage
