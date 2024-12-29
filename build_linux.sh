#!/bin/bash

echo "Building TubeMaster Pro for Linux..."

# Install required dependencies
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip python3-venv build-essential

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Build the application
pyinstaller --clean --noconfirm "TubeMaster Pro.spec"

# Create .desktop file
cat > "TubeMaster Pro.desktop" << EOF
[Desktop Entry]
Name=TubeMaster Pro
Exec=TubeMaster Pro
Icon=/usr/share/icons/tubemaster.png
Type=Application
Categories=Utility;
Comment=Modern YouTube Video Downloader
EOF

# Create AppImage
wget -c "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
chmod +x linuxdeploy-x86_64.AppImage

# Create AppDir structure
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Copy files
cp -r "dist/TubeMaster Pro"/* AppDir/usr/bin/
cp "TubeMaster Pro.desktop" AppDir/usr/share/applications/
cp assets/app_icon.png AppDir/usr/share/icons/hicolor/256x256/apps/tubemaster.png

# Create AppImage
./linuxdeploy-x86_64.AppImage --appdir AppDir --output appimage

# Create DEB package
mkdir -p debian/DEBIAN
cat > debian/DEBIAN/control << EOF
Package: tubemaster-pro
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Telvin Teum
Description: Modern YouTube Video Downloader
 A professional YouTube video downloader with modern UI.
EOF

mkdir -p debian/usr/bin
mkdir -p debian/usr/share/applications
mkdir -p debian/usr/share/icons/hicolor/256x256/apps

cp -r "dist/TubeMaster Pro"/* debian/usr/bin/
cp "TubeMaster Pro.desktop" debian/usr/share/applications/
cp assets/app_icon.png debian/usr/share/icons/hicolor/256x256/apps/tubemaster.png

dpkg-deb --build debian tubemaster-pro_1.0.0_amd64.deb

echo "Build complete! Check the following files:"
echo "1. AppImage: TubeMaster_Pro-x86_64.AppImage"
echo "2. DEB package: tubemaster-pro_1.0.0_amd64.deb"
echo "3. Standalone executable: dist/TubeMaster Pro/TubeMaster Pro"
