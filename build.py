import os
import sys
import platform
from pathlib import Path

def get_platform():
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'macos'
    else:
        return 'linux'

def build_app():
    platform_name = get_platform()
    app_name = "TubeMaster Pro"
    version = "1.0.0"
    
    # Base PyInstaller command
    base_command = f"""pyinstaller --noconfirm --clean --name "{app_name}" """
    base_command += "--hidden-import=PySide6.QtCore "
    base_command += "--hidden-import=PySide6.QtGui "
    base_command += "--hidden-import=PySide6.QtWidgets "
    base_command += "--hidden-import=yt_dlp "
    
    # Add icon
    if platform_name == 'windows':
        base_command += "--icon=assets/app_icon.ico "
    elif platform_name == 'macos':
        base_command += "--icon=assets/app_icon.icns "
    else:
        base_command += "--icon=assets/app_icon.png "
    
    # Platform specific options
    if platform_name == 'windows':
        base_command += "--windowed "  # No console window
        base_command += "--add-data 'assets;assets' "
    elif platform_name == 'macos':
        base_command += "--windowed "
        base_command += "--add-data 'assets:assets' "
        base_command += f"--osx-bundle-identifier 'com.telvin.{app_name.lower().replace(' ', '')}' "
    else:  # Linux
        base_command += "--add-data 'assets:assets' "
    
    # Main script
    base_command += "main.py"
    
    # Create spec file
    print("Creating spec file...")
    os.system(base_command)
    
    # Build the app
    print("Building application...")
    os.system("pyinstaller --clean --noconfirm TubeMaster\\ Pro.spec")
    
    print(f"Build completed for {platform_name}!")
    print(f"Output can be found in the 'dist' directory")

if __name__ == "__main__":
    build_app()
