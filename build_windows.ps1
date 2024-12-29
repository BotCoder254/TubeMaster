# Windows Build Script for TubeMaster Pro

Write-Host "Building TubeMaster Pro for Windows..."

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install pywin32

# Build the application
pyinstaller --clean --noconfirm "TubeMaster Pro.spec"

# Create Inno Setup script
$INNO_SCRIPT = @"
[Setup]
AppName=TubeMaster Pro
AppVersion=1.0.0
DefaultDirName={pf}\TubeMaster Pro
DefaultGroupName=TubeMaster Pro
OutputDir=output
OutputBaseFilename=TubeMaster_Pro_Setup
SetupIconFile=assets\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\TubeMaster Pro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\TubeMaster Pro"; Filename: "{app}\TubeMaster Pro.exe"
Name: "{autodesktop}\TubeMaster Pro"; Filename: "{app}\TubeMaster Pro.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\TubeMaster Pro.exe"; Description: "{cm:LaunchProgram,TubeMaster Pro}"; Flags: nowait postinstall skipifsilent
"@

# Save Inno Setup script
$INNO_SCRIPT | Out-File -Encoding UTF8 "installer.iss"

# Check if Inno Setup is installed
$INNO_PATH = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (Test-Path $INNO_PATH) {
    Write-Host "Creating installer..."
    & $INNO_PATH "installer.iss"
} else {
    Write-Host "Inno Setup not found. Please install it to create the installer."
    Write-Host "Download from: https://jrsoftware.org/isdl.php"
}

Write-Host "Build complete! Check the following:"
Write-Host "1. Standalone executable: dist\TubeMaster Pro\TubeMaster Pro.exe"
Write-Host "2. Installer (if Inno Setup was available): output\TubeMaster_Pro_Setup.exe"
