import os
import subprocess
from PIL import Image

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_icons():
    """Generate icons for all platforms using Inkscape or convert"""
    print("Generating icons for all platforms...")
    
    # Ensure assets directory exists
    ensure_dir('assets/icons')
    
    # Source SVG file
    svg_path = 'assets/logo.svg'
    
    if not os.path.exists(svg_path):
        print(f"Error: SVG file not found at {svg_path}")
        return
    
    # Try using Inkscape first, then ImageMagick's convert
    def convert_svg(output_path, size):
        try:
            # Try Inkscape first
            if subprocess.run(['which', 'inkscape'], capture_output=True).returncode == 0:
                subprocess.run([
                    'inkscape',
                    '--export-filename=' + output_path,
                    '-w', str(size),
                    '-h', str(size),
                    svg_path
                ], check=True)
                return True
            # Try ImageMagick's convert
            elif subprocess.run(['which', 'convert'], capture_output=True).returncode == 0:
                subprocess.run([
                    'convert',
                    '-background', 'none',
                    '-resize', f'{size}x{size}',
                    svg_path,
                    output_path
                ], check=True)
                return True
        except subprocess.CalledProcessError:
            return False
        return False

    # Windows ICO
    sizes = [16, 24, 32, 48, 64, 128, 256]
    ico_images = []
    
    for size in sizes:
        png_path = f'assets/icons/icon_{size}x{size}.png'
        if convert_svg(png_path, size):
            ico_images.append(Image.open(png_path))
    
    if ico_images:
        # Save ICO file
        ico_images[0].save('assets/app_icon.ico', format='ICO', sizes=[(s, s) for s in sizes], 
                          append_images=ico_images[1:])
        print("Created Windows ICO file")
    
    # macOS ICNS sizes
    icns_sizes = {
        '16x16': '16x16.png',
        '32x32': '16x16@2x.png',
        '32x32': '32x32.png',
        '64x64': '32x32@2x.png',
        '128x128': '128x128.png',
        '256x256': '128x128@2x.png',
        '256x256': '256x256.png',
        '512x512': '256x256@2x.png',
        '512x512': '512x512.png',
        '1024x1024': '512x512@2x.png'
    }
    
    iconset_path = 'assets/icons/icon.iconset'
    ensure_dir(iconset_path)
    
    for size, filename in icns_sizes.items():
        width = int(size.split('x')[0])
        png_path = os.path.join(iconset_path, f'icon_{filename}')
        convert_svg(png_path, width)
    
    # Create ICNS file on macOS
    if os.system('which iconutil') == 0:  # macOS
        os.system(f'iconutil -c icns {iconset_path} -o assets/app_icon.icns')
        print("Created macOS ICNS file")
    
    # Linux PNG (512x512)
    if convert_svg('assets/app_icon.png', 512):
        print("Created Linux PNG file")
    
    print("Icon generation complete!")
    print("\nPlease install one of the following to convert SVG to PNG:")
    print("1. Inkscape (recommended):")
    print("   sudo apt-get install inkscape")
    print("2. Or ImageMagick:")
    print("   sudo apt-get install imagemagick")

if __name__ == "__main__":
    generate_icons()
