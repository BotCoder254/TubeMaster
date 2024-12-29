# TubeMaster Pro Build Guide

This guide explains how to build TubeMaster Pro for Linux, Windows, and macOS platforms.

## Prerequisites

### All Platforms
- Python 3.8 or higher
- Git

### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip python3-venv build-essential \
    libcairo2-dev libgirepository1.0-dev pkg-config gir1.2-gtk-3.0

# Fedora
sudo dnf install python3-devel python3-pip python3-virtualenv \
    cairo-devel gobject-introspection-devel pkg-config gtk3
```

### Windows
- Python 3.8+ (with PATH option enabled during installation)
- [Inno Setup](https://jrsoftware.org/isdl.php) (for creating installer)
- Visual Studio Build Tools (will be installed automatically if needed)

### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install cairo pkg-config
brew install create-dmg  # For creating DMG installer
```

## Build Steps

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/tubemaster-pro.git
cd tubemaster-pro
```

### 2. Automated Build (Recommended)

The automated build script will handle everything for your current platform:

```bash
python build_all.py
```

### 3. Manual Platform-Specific Builds

#### Linux Build
```bash
# Make script executable
chmod +x build_linux.sh

# Run build script
./build_linux.sh
```

Outputs:
- Standalone executable: `dist/TubeMaster Pro/TubeMaster Pro`
- AppImage: `TubeMaster_Pro-x86_64.AppImage`
- DEB package: `tubemaster-pro_1.0.0_amd64.deb`

#### Windows Build
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
.\build_windows.ps1
```

Outputs:
- Standalone executable: `dist\TubeMaster Pro\TubeMaster Pro.exe`
- Installer: `output\TubeMaster_Pro_Setup.exe`

#### macOS Build
```bash
# Make script executable
chmod +x build_macos.sh

# Run build script
./build_macos.sh
```

Outputs:
- Application bundle: `dist/TubeMaster Pro.app`
- DMG installer: `TubeMaster Pro.dmg`

## Icon Generation

The build process includes automatic icon generation from the SVG logo. If you need to generate icons manually:

```bash
python generate_icons.py
```

This will create:
- Windows: `assets/app_icon.ico`
- macOS: `assets/app_icon.icns`
- Linux: `assets/app_icon.png`

## Troubleshooting

### Linux
- If you get cairo errors: `sudo apt-get install libcairo2-dev`
- If AppImage creation fails: Check if `linuxdeploy` is downloaded and executable

### Windows
- If PyInstaller fails: Install Visual Studio Build Tools
- If Inno Setup is not found: Add Inno Setup to PATH or provide full path in build script

### macOS
- If icon conversion fails: Ensure you have `iconutil` installed
- If DMG creation fails: `brew install create-dmg`

## Distribution

### Linux
- AppImage: Universal format, works on most Linux distributions
- DEB: For Debian-based systems (Ubuntu, Linux Mint, etc.)
- Standalone: Can be run directly, requires dependencies

### Windows
- Installer: Recommended for most users
- Standalone: Portable version, no installation required

### macOS
- DMG: Standard distribution format
- App Bundle: Can be copied directly to Applications folder

## Notes

- Builds are created in the `dist` directory
- Each platform has its own icon format
- Code signing is available for macOS (requires Developer ID)
- Windows installer includes Start Menu integration
- Linux builds include desktop integration

## Support

For build-related issues:
1. Check the prerequisites are installed
2. Ensure all dependencies are met
3. Check the build logs in the `build_logs` directory
4. Create an issue on GitHub if problems persist

## Building TubeMaster Pro

This document describes how to build TubeMaster Pro from source for different platforms.

### Prerequisites

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt-get update

# Install required dependencies
sudo apt-get install -y python3-dev python3-pip python3-venv build-essential \
    inkscape imagemagick python3-setuptools libcairo2-dev \
    libgirepository1.0-dev pkg-config gir1.2-gtk-3.0
```

#### macOS
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required dependencies
brew install create-dmg inkscape
```

#### Windows
1. Install Python 3.8 or later from [python.org](https://www.python.org/downloads/)
2. Install Inno Setup from [jrsoftware.org](https://jrsoftware.org/isdl.php)

### Building the Application

#### Automatic Build (Recommended)

The easiest way to build TubeMaster Pro is using the automated build script:

```bash
# Make the build script executable (Linux/macOS only)
chmod +x build_all.py

# Run the build script
python3 build_all.py
```

The build script will:
1. Check and install required system dependencies
2. Set up a Python virtual environment
3. Install required Python packages
4. Generate application icons
5. Create platform-specific builds
6. Package the application

#### Manual Build

If you prefer to build manually, follow these steps:

1. Set up Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

2. Install dependencies:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3. Generate icons:
```bash
python generate_icons.py
```

4. Create PyInstaller build:
```bash
pyinstaller "TubeMaster Pro.spec"
```

### Build Outputs

After a successful build, you'll find:

- **Linux**: AppImage in `output/linux/`
- **Windows**: 
  - Installer: `output/windows/TubeMasterProSetup.exe`
  - Portable: `output/windows/TubeMasterProPortable.zip`
- **macOS**: DMG file in `output/macos/`

### Troubleshooting

#### Common Issues

1. **Missing Dependencies**
   - Run the build script with `--verbose` flag for detailed output
   - Check system requirements are installed
   - Ensure Python version is 3.8 or later

2. **Icon Generation Fails**
   - Verify Inkscape or ImageMagick is installed
   - Check SVG source files exist in assets directory

3. **Build Process Fails**
   - Check Python virtual environment is activated
   - Verify all dependencies are installed
   - Check disk space availability

### Getting Help

If you encounter issues:
1. Check the error messages in the console
2. Review the build log in `build/build.log`
3. Open an issue on the project repository

### Development Build

For development and testing:

```bash
# Create development build
python3 build_all.py --dev

# Run tests
python3 -m pytest tests/
```

### Custom Build Options

The build script supports several options:

```bash
python3 build_all.py [options]

Options:
  --dev           Create development build
  --no-clean      Skip cleaning build directories
  --verbose       Show detailed build output
  --skip-tests    Skip running tests
