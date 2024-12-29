<div align="center">
  <img src="assets/logo.svg" alt="TubeMaster Pro Logo" width="200" height="200"/>
</div>

# TubeMaster Pro

<div align="center">
  
  [![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
  [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
  [![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/yourusername/tubemaster-pro)
  [![Made with Qt](https://img.shields.io/badge/Made%20with-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://www.qt.io)
  
</div>

<div align="center">
  <h2>🎥 A Modern YouTube Video Downloader with Style</h2>
  <p align="center">
    <b>Built with cutting-edge technology for the best download experience</b>
    <br />
    <i>Coded with ❤️ by Telvin Teum</i>
  </p>
</div>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## ✨ Key Features

<div align="center">
  <table>
    <tr>
      <td align="center">🎯</td>
      <td><b>Smart Search</b></td>
      <td>Real-time video search with thumbnails and details</td>
    </tr>
    <tr>
      <td align="center">📊</td>
      <td><b>Quality Options</b></td>
      <td>Multiple video formats and quality selections</td>
    </tr>
    <tr>
      <td align="center">💫</td>
      <td><b>Modern UI</b></td>
      <td>Clean, dark-themed interface with smooth animations</td>
    </tr>
    <tr>
      <td align="center">📂</td>
      <td><b>Smart Downloads</b></td>
      <td>Intelligent file management and organization</td>
    </tr>
    <tr>
      <td align="center">🔄</td>
      <td><b>Live Progress</b></td>
      <td>Real-time download tracking with speed and ETA</td>
    </tr>
  </table>
</div>

## 🎯 Key Features Explained

### Video Search
- Asynchronous search functionality
- Real-time thumbnail loading
- Detailed video information display
- Smart URL validation and error handling
- Preview thumbnails before downloading

### Download Management
- Custom download directory selection
- Intelligent file naming system
- Duplicate file handling
- Progress tracking and notifications
- Smart file organization
- Custom save location selection
- Real-time progress updates
- Download speed and ETA display
- Automatic file naming conflict resolution

### User Interface
- Dark theme for reduced eye strain
- Responsive layout design
- Interactive progress indicators
- Modern notification system
- Clean and intuitive controls
- Custom styled components
- Smooth animations and transitions
- Real-time status updates
- Error handling with user feedback

### Technical Features
- Asynchronous video processing
- Multi-threaded downloads
- Memory-efficient thumbnail handling
- Smart error recovery
- Format auto-selection
- Quality preference handling
- Network error handling
- Session management

## 🛠️ Technical Details

### Dependencies
- **PySide6**: Modern Qt-based UI framework for the graphical interface
- **yt-dlp**: Advanced YouTube download library with format selection
- **requests**: HTTP library for thumbnail fetching and API calls
- **Pillow**: Image processing for thumbnails and previews

### System Requirements
- Python 3.8 or higher
- Qt 6.0+ (via PySide6)
- Internet connection
- Supported OS: Linux, Windows, macOS
- Minimum 2GB RAM
- 100MB free disk space

### Installation Details
1. **System Prerequisites**
   - Python 3.8+ installed
   - pip package manager
   - Virtual environment (recommended)

2. **Dependencies Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Platform-Specific Setup**
   - Linux: No additional setup needed
   - Windows: May require Microsoft Visual C++ Redistributable
   - macOS: Requires Xcode Command Line Tools

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/tubemaster-pro.git

# Navigate to directory
cd tubemaster-pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 💻 Usage Guide

### Basic Usage
1. Launch the application
2. Paste a YouTube URL
3. Click "Search" to load video details
4. Select preferred quality
5. Click "Download" to start

### Advanced Features
1. **Custom Download Location**
   - Click the folder icon
   - Select preferred directory
   - All downloads will save there

2. **Quality Selection**
   - Choose from available formats
   - See file size estimates
   - Preview quality options

3. **Download Management**
   - Monitor progress in real-time
   - See download speed
   - View estimated time
   - Cancel downloads
   - Open download location

4. **Error Handling**
   - Clear error messages
   - Automatic retry options
   - Network error recovery
   - Invalid URL detection

## 🔧 Configuration

### Default Settings
- Download Path: `~/Downloads/TubeMaster`
- Default Quality: Highest available
- Auto-close notifications: 10 seconds
- Maximum concurrent downloads: 1

### Customization Options
- Change download location
- Select preferred quality
- Modify notification duration
- Adjust window size

## 🚀 Performance

### Optimizations
- Efficient memory usage
- Smart thumbnail caching
- Asynchronous operations
- Multi-threaded downloads

### Limitations
- Single video download at a time
- Network-dependent performance
- Platform-specific behaviors

## 🛡️ Security

### Features
- Safe file handling
- Secure downloads
- No data collection
- Local-only operation

### Compliance
- YouTube Terms of Service
- Local privacy laws
- Data protection standards

## 💻 Preview

<div align="center">
  <table>
    <tr>
      <td align="center">
        <b>Dark Theme</b><br>
        <img src="assets/dark-theme.png" alt="Dark Theme" width="400"/>
      </td>
      <td align="center">
        <b>Download Manager</b><br>
        <img src="assets/download.png" alt="Download Manager" width="400"/>
      </td>
    </tr>
  </table>
</div>

## 🛠️ Technology Stack

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png" width="40" alt="Python"/></td>
      <td align="center"><img src="https://upload.wikimedia.org/wikipedia/commons/0/0b/Qt_logo_2016.svg" width="40" alt="Qt"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/logo.png" width="40" alt="yt-dlp"/></td>
    </tr>
    <tr>
      <td align="center">Python 3.8+</td>
      <td align="center">PySide6 (Qt)</td>
      <td align="center">yt-dlp</td>
    </tr>
  </table>
</div>

## 📋 Upcoming Features

<div align="center">
  <table>
    <tr>
      <td>⏳ Playlist Support</td>
      <td>🔄 Download Queue</td>
      <td>⚙️ User Preferences</td>
      <td>🌐 More Platforms</td>
      <td>🔍 Advanced Search</td>
    </tr>
  </table>
</div>

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for ways to get started.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/yourusername">
          <img src="https://github.com/yourusername.png" width="100px;" alt="Telvin Teum"/>
          <br />
          <b>Telvin Teum</b>
        </a>
      </td>
    </tr>
  </table>
</div>

---

<div align="center">
  <p>
    <a href="https://github.com/yourusername/tubemaster-pro/issues">Report Bug</a>
    ·
    <a href="https://github.com/yourusername/tubemaster-pro/issues">Request Feature</a>
  </p>
  
  <p>If you like this project, give it a ⭐!</p>
  
  <p>
    <sub>Copyright © 2024 TubeMaster Pro. All rights reserved.</sub>
  </p>
</div>
