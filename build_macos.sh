#!/bin/bash

echo "Building TubeMaster Pro for macOS..."

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install create-dmg if not installed
if ! command -v create-dmg &> /dev/null; then
    brew install create-dmg
fi

# Build the application
pyinstaller --clean --noconfirm "TubeMaster Pro.spec"

# Create Info.plist
cat > "dist/TubeMaster Pro.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>TubeMaster Pro</string>
    <key>CFBundleDisplayName</key>
    <string>TubeMaster Pro</string>
    <key>CFBundleIdentifier</key>
    <string>com.telvin.tubemasterpro</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleExecutable</key>
    <string>TubeMaster Pro</string>
    <key>CFBundleIconFile</key>
    <string>app_icon.icns</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.12.0</string>
</dict>
</plist>
EOF

# Convert icon to icns if needed
if [ -f "assets/app_icon.png" ]; then
    mkdir icon.iconset
    sips -z 16 16   assets/app_icon.png --out icon.iconset/icon_16x16.png
    sips -z 32 32   assets/app_icon.png --out icon.iconset/icon_16x16@2x.png
    sips -z 32 32   assets/app_icon.png --out icon.iconset/icon_32x32.png
    sips -z 64 64   assets/app_icon.png --out icon.iconset/icon_32x32@2x.png
    sips -z 128 128 assets/app_icon.png --out icon.iconset/icon_128x128.png
    sips -z 256 256 assets/app_icon.png --out icon.iconset/icon_128x128@2x.png
    sips -z 256 256 assets/app_icon.png --out icon.iconset/icon_256x256.png
    sips -z 512 512 assets/app_icon.png --out icon.iconset/icon_256x256@2x.png
    sips -z 512 512 assets/app_icon.png --out icon.iconset/icon_512x512.png
    sips -z 1024 1024 assets/app_icon.png --out icon.iconset/icon_512x512@2x.png
    iconutil -c icns icon.iconset
    cp icon.icns "dist/TubeMaster Pro.app/Contents/Resources/app_icon.icns"
    rm -rf icon.iconset
fi

# Sign the application (if certificate is available)
if [ -n "$APPLE_DEVELOPER_ID" ]; then
    codesign --force --sign "$APPLE_DEVELOPER_ID" --deep "dist/TubeMaster Pro.app"
    echo "Application signed with Developer ID"
else
    echo "No Developer ID found. Skipping code signing."
fi

# Create DMG
create-dmg \
    --volname "TubeMaster Pro" \
    --volicon "icon.icns" \
    --window-pos 200 120 \
    --window-size 800 400 \
    --icon-size 100 \
    --icon "TubeMaster Pro.app" 200 190 \
    --hide-extension "TubeMaster Pro.app" \
    --app-drop-link 600 185 \
    "TubeMaster Pro.dmg" \
    "dist/TubeMaster Pro.app"

echo "Build complete! Check the following:"
echo "1. Application bundle: dist/TubeMaster Pro.app"
echo "2. DMG installer: TubeMaster Pro.dmg"
