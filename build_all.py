import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def get_platform():
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'macos'
    else:
        return 'linux'

def run_command(command, cwd=None, shell=False):
    """Run a command and return its success status and output"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
            check=False,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_linux_dependencies():
    """Install required Linux dependencies"""
    print("Installing Linux dependencies...")
    
    dependencies = [
        'python3-dev',
        'python3-pip',
        'python3-venv',
        'build-essential',
        'inkscape',
        'imagemagick',
        'python3-setuptools',  # Added setuptools
        'libcairo2-dev',
        'libgirepository1.0-dev',
        'pkg-config',
        'gir1.2-gtk-3.0'
    ]
    
    print("\nRunning system update and installing dependencies...")
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y'] + dependencies, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError installing dependencies: {str(e)}")
        print("\nPlease run these commands manually:")
        print("\nsudo apt-get update")
        print(f"sudo apt-get install -y {' '.join(dependencies)}")
        return False

def ensure_dependencies():
    """Ensure all required system dependencies are installed"""
    platform = get_platform()
    
    if platform == 'linux':
        print("Checking Linux dependencies...")
        
        # Check for Inkscape or ImageMagick
        has_inkscape, _, _ = run_command(['which', 'inkscape'])
        has_imagemagick, _, _ = run_command(['which', 'convert'])
        
        if not (has_inkscape or has_imagemagick):
            print("Neither Inkscape nor ImageMagick found. Attempting to install dependencies...")
            if not install_linux_dependencies():
                return False
    
    return True

def setup_python_environment():
    """Setup Python virtual environment and install dependencies"""
    print("Setting up Python environment...")
    
    # Deactivate current virtual environment if active
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Deactivating current virtual environment...")
        if get_platform() == 'windows':
            os.system('deactivate')
        else:
            os.system('deactivate 2>/dev/null || true')
    
    # Remove existing virtual environment if it exists
    if os.path.exists('venv'):
        print("Removing existing virtual environment...")
        shutil.rmtree('venv')
    
    print("Creating new virtual environment...")
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
    
    # Get the correct pip path
    if sys.platform.startswith('win'):
        python_cmd = os.path.join('venv', 'Scripts', 'python')
        pip_cmd = os.path.join('venv', 'Scripts', 'pip')
    else:
        python_cmd = os.path.join('venv', 'bin', 'python')
        pip_cmd = os.path.join('venv', 'bin', 'pip')
    
    print("Installing base packages...")
    subprocess.run([python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'], check=True)
    
    print("Installing project requirements...")
    subprocess.run([pip_cmd, 'install', '-r', 'requirements.txt'], check=True)
    
    return True

def setup_environment():
    print("Setting up build environment...")
    
    # Create necessary directories
    directories = ['assets', 'dist', 'build', 'output']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Check and install system dependencies
    if not ensure_dependencies():
        print("Please install required dependencies and try again.")
        sys.exit(1)
    
    # Setup Python environment
    if not setup_python_environment():
        print("Failed to setup Python environment.")
        sys.exit(1)
    
    print("Activating virtual environment...")
    if get_platform() == 'windows':
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        os.system(f'"{activate_script}"')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
        os.system(f'source "{activate_script}"')
    
    # Generate icons
    print("Generating application icons...")
    subprocess.run([sys.executable, 'generate_icons.py'])
    
    # Create spec file if it doesn't exist
    if not os.path.exists('TubeMaster Pro.spec'):
        create_spec_file()

def create_spec_file():
    print("Creating PyInstaller spec file...")
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'yt_dlp'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TubeMaster Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app_icon.ico' if sys.platform.startswith('win') else 'assets/app_icon.icns' if sys.platform.startswith('darwin') else 'assets/app_icon.png'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TubeMaster Pro',
)

if sys.platform.startswith('darwin'):
    app = BUNDLE(
        coll,
        name='TubeMaster Pro.app',
        icon='assets/app_icon.icns',
        bundle_identifier='com.telvin.tubemasterpro',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.12.0',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSRequiresAquaSystemAppearance': 'No',
            'NSMicrophoneUsageDescription': 'TubeMaster Pro does not use the microphone.',
            'NSCameraUsageDescription': 'TubeMaster Pro does not use the camera.',
        },
    )
"""
    with open('TubeMaster Pro.spec', 'w') as f:
        f.write(spec_content)

def create_desktop_file():
    """Create .desktop file for Linux"""
    desktop_content = """[Desktop Entry]
Name=TubeMaster Pro
Exec=TubeMaster Pro
Icon=tubemaster
Type=Application
Categories=Utility;
Comment=Modern YouTube Video Downloader
"""
    with open('TubeMaster Pro.desktop', 'w') as f:
        f.write(desktop_content)

def build_windows():
    print("Building for Windows...")
    
    # Create a simple LICENSE file if it doesn't exist
    if not os.path.exists('LICENSE'):
        with open('LICENSE', 'w') as f:
            f.write("MIT License\nCopyright (c) 2024 Telvin Teum\n")
    
    # Build with PyInstaller
    subprocess.run(['pyinstaller', '--clean', '--noconfirm', 'TubeMaster Pro.spec'])
    
    # Create Inno Setup script
    inno_script = """#define MyAppName "TubeMaster Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Telvin Teum"
#define MyAppURL "https://github.com/telvin/tubemaster-pro"
#define MyAppExeName "TubeMaster Pro.exe"

[Setup]
AppId={{A4D0F5A2-1234-5678-9ABC-DEF123456789}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=output
OutputBaseFilename=TubeMaster_Pro_Setup
SetupIconFile=assets\\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\{#MyAppName}\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
"""
    with open('installer.iss', 'w') as f:
        f.write(inno_script)
    
    # Create output directory for installer
    os.makedirs('output', exist_ok=True)
    
    # Check if Inno Setup is installed
    inno_paths = [
        r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        r'C:\Program Files\Inno Setup 6\ISCC.exe'
    ]
    
    inno_compiler = None
    for path in inno_paths:
        if os.path.exists(path):
            inno_compiler = path
            break
    
    if inno_compiler:
        print("Creating Windows installer...")
        subprocess.run([inno_compiler, 'installer.iss'])
        print("Installer created successfully!")
    else:
        print("Inno Setup not found. Standalone executable is available in dist/TubeMaster Pro/")
        print("To create an installer, please install Inno Setup from: https://jrsoftware.org/isdl.php")
    
    # Create portable version
    portable_dir = 'output/TubeMaster Pro Portable'
    os.makedirs(portable_dir, exist_ok=True)
    
    # Copy all files to portable directory
    if os.path.exists('dist/TubeMaster Pro'):
        shutil.copytree('dist/TubeMaster Pro', portable_dir, dirs_exist_ok=True)
    
    # Create portable marker file
    with open(os.path.join(portable_dir, 'portable.txt'), 'w') as f:
        f.write('This is a portable version of TubeMaster Pro')
    
    # Create ZIP archive of portable version
    shutil.make_archive('output/TubeMaster_Pro_Portable', 'zip', portable_dir)
    
    print("\nWindows build completed!")
    print("Output files:")
    print("1. Installer: output/TubeMaster_Pro_Setup.exe (if Inno Setup was available)")
    print("2. Portable version: output/TubeMaster_Pro_Portable.zip")
    print("3. Standalone executable: dist/TubeMaster Pro/TubeMaster Pro.exe")

def build_linux():
    print("Building for Linux...")
    
    # Build with PyInstaller
    subprocess.run(['pyinstaller', '--clean', '--noconfirm', 'TubeMaster Pro.spec'])
    
    # Ensure icon exists
    if not os.path.exists('assets/app_icon.png'):
        print("Error: Icon file missing. Running icon generation...")
        subprocess.run([sys.executable, 'generate_icons.py'])
    
    # Copy files to AppDir
    os.makedirs('AppDir/usr/bin', exist_ok=True)
    os.makedirs('AppDir/usr/share/applications', exist_ok=True)
    os.makedirs('AppDir/usr/share/icons/hicolor/256x256/apps', exist_ok=True)
    
    # Copy application files
    if os.path.exists('dist/TubeMaster Pro'):
        for item in os.listdir('dist/TubeMaster Pro'):
            src = os.path.join('dist/TubeMaster Pro', item)
            dst = os.path.join('AppDir/usr/bin', item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
    
    # Copy desktop file and icon
    shutil.copy2('TubeMaster Pro.desktop', 'AppDir/usr/share/applications/')
    shutil.copy2('assets/app_icon.png', 
                'AppDir/usr/share/icons/hicolor/256x256/apps/tubemaster.png')
    
    # Download and prepare AppImage tools
    if not os.path.exists('linuxdeploy-x86_64.AppImage'):
        subprocess.run(['wget', 'https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage'])
        os.chmod('linuxdeploy-x86_64.AppImage', 0o755)
    
    # Create AppImage
    subprocess.run(['./linuxdeploy-x86_64.AppImage', 
                   '--appdir', 'AppDir',
                   '--output', 'appimage'])

def build_macos():
    print("Building for macOS...")
    
    # Build with PyInstaller
    subprocess.run(['pyinstaller', '--clean', '--noconfirm', 'TubeMaster Pro.spec'])
    
    # Create DMG if create-dmg is available
    if subprocess.run(['which', 'create-dmg'], capture_output=True).returncode == 0:
        print("Creating DMG installer...")
        
        # Clean up any existing DMG
        dmg_path = 'output/TubeMaster Pro.dmg'
        if os.path.exists(dmg_path):
            os.remove(dmg_path)
        
        # Create DMG
        subprocess.run([
            'create-dmg',
            '--volname', 'TubeMaster Pro',
            '--volicon', 'assets/app_icon.icns',
            '--background', 'assets/dmg-background.png',
            '--window-pos', '200', '120',
            '--window-size', '800', '400',
            '--icon-size', '100',
            '--icon', 'TubeMaster Pro.app', '200', '190',
            '--hide-extension', 'TubeMaster Pro.app',
            '--app-drop-link', '600', '185',
            dmg_path,
            'dist/TubeMaster Pro.app'
        ])
        
        print(f"DMG installer created: {dmg_path}")
    else:
        print("create-dmg not found. Skipping DMG creation.")
        print("Install with: brew install create-dmg")
    
    # Optionally sign the application if certificate is available
    if os.environ.get('APPLE_DEVELOPER_ID'):
        print("Signing application with Developer ID...")
        subprocess.run([
            'codesign',
            '--force',
            '--sign', os.environ['APPLE_DEVELOPER_ID'],
            '--deep',
            '--options', 'runtime',
            'dist/TubeMaster Pro.app'
        ])
        
        if os.path.exists(dmg_path):
            print("Signing DMG...")
            subprocess.run([
                'codesign',
                '--force',
                '--sign', os.environ['APPLE_DEVELOPER_ID'],
                dmg_path
            ])
    
    print("\nmacOS build completed!")
    print("Output files:")
    print("1. Application bundle: dist/TubeMaster Pro.app")
    if os.path.exists(dmg_path):
        print(f"2. DMG installer: {dmg_path}")

def main():
    # Setup environment
    setup_environment()
    
    # Determine platform and build
    current_platform = get_platform()
    
    if current_platform == 'linux':
        build_linux()
    elif current_platform == 'windows':
        build_windows()
    elif current_platform == 'macos':
        build_macos()
    
    print("\nBuild process completed!")
    print("\nBuild outputs can be found in:")
    print("- Linux: dist/TubeMaster Pro/ (executable), *.AppImage")
    print("- Windows: dist/TubeMaster Pro/ (executable), output/TubeMaster_Pro_Setup.exe")
    print("- macOS: dist/TubeMaster Pro.app, output/TubeMaster Pro.dmg")

if __name__ == "__main__":
    main()
