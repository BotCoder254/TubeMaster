import sys
import os
import yt_dlp
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QComboBox, QProgressBar, QScrollArea, QMessageBox,
                             QFrame, QSizePolicy, QFileDialog, QToolTip)
from PySide6.QtCore import Qt, QThread, Signal, QPropertyAnimation, QEasingCurve, QSize, QTimer, QByteArray, QRectF
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor, QPen, QBrush, QPainterPath
from PySide6.QtSvg import QSvgRenderer

# Define SVG icons directly in the code since the resources module might not be loading correctly
YOUTUBE_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path fill="#FF0000" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
</svg>
"""

DOWNLOAD_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path fill="#FFFFFF" d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
</svg>
"""

SEARCH_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path fill="#FFFFFF" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
</svg>
"""

LOCATION_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path fill="#FFFFFF" d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"/>
</svg>
"""

def create_svg_icon(svg_data, size):
    renderer = QSvgRenderer(QByteArray(svg_data.encode()))
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap

class CustomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            CustomFrame {
                background-color: #3b3b3b;
                border-radius: 10px;
                border: 1px solid #555555;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

class SpinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.setInterval(50)  # 20 fps
        self.setFixedSize(40, 40)
        self.color = QColor("#FF0000")  # YouTube red

    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        self.timer.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create a circular path
        path = QPainterPath()
        rect = QRectF(5, 5, self.width() - 10, self.height() - 10)
        path.addEllipse(rect)
        
        # Set up the pen
        pen = QPen(self.color)
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        
        # Rotate and draw the arc
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        painter.translate(-self.width() / 2, -self.height() / 2)
        
        # Draw the spinning arc
        painter.strokePath(path, pen)
        
        # Draw small circles at the ends
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect.center(), 3, 3)

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Semi-transparent background
        self.background = QWidget(self)
        self.background.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Center container
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setSpacing(15)
        
        # Spinner widget
        self.spinner = SpinnerWidget()
        center_layout.addWidget(self.spinner, alignment=Qt.AlignCenter)
        
        # Loading text
        self.loading_text = QLabel("Loading...")
        self.loading_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        center_layout.addWidget(self.loading_text, alignment=Qt.AlignCenter)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 5px;
                text-align: center;
                height: 20px;
                min-width: 300px;
                max-width: 400px;
                background-color: #3b3b3b;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #FF0000;
                border-radius: 3px;
            }
        """)
        center_layout.addWidget(self.progress, alignment=Qt.AlignCenter)
        
        layout.addWidget(center_container, alignment=Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

    def set_progress(self, value, text):
        self.progress.setValue(int(value))
        self.loading_text.setText(text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.setGeometry(self.rect())

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"size")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        self.default_size = QSize(self.sizeHint().width(), self.sizeHint().height())

    def enterEvent(self, event):
        self._animation.setStartValue(self.size())
        self._animation.setEndValue(QSize(int(self.default_size.width() * 1.1),
                                        int(self.default_size.height() * 1.1)))
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setStartValue(self.size())
        self._animation.setEndValue(self.default_size)
        self._animation.start()
        super().leaveEvent(event)

class SearchWorker(QThread):
    progress = Signal(float, str)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            self.progress.emit(10, "Initializing search...")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False
            }
            
            self.progress.emit(30, "Fetching video information...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(self.url, download=False)
            
            self.progress.emit(60, "Processing video details...")
            
            # Fetch thumbnail
            thumbnail_url = video_info.get('thumbnail')
            thumbnail_data = None
            if thumbnail_url:
                self.progress.emit(80, "Loading thumbnail...")
                response = requests.get(thumbnail_url)
                img = Image.open(BytesIO(response.content))
                img = img.resize((720, 405), Image.Resampling.LANCZOS)
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                thumbnail_data = img_byte_arr.getvalue()
            
            self.progress.emit(100, "Complete!")
            self.finished.emit({
                'info': video_info,
                'thumbnail': thumbnail_data
            })
            
        except Exception as e:
            self.error.emit(str(e))

class DownloadWorker(QThread):
    progress = Signal(float, str)  # Progress percentage and status message
    finished = Signal()
    error = Signal(str)

    def __init__(self, url, format_id, save_path, video_info):
        super().__init__()
        self.url = url
        self.format_id = format_id
        self.save_path = save_path
        self.video_info = video_info

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                # Calculate progress
                if 'total_bytes' in d:
                    percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif 'total_bytes_estimate' in d:
                    percentage = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                else:
                    percentage = 0
                
                # Create status message
                speed = d.get('speed', 0)
                if speed:
                    speed_str = self.format_size(speed) + '/s'
                else:
                    speed_str = '-- B/s'
                
                eta = d.get('eta', 0)
                if eta:
                    eta_str = f'{eta//60}:{eta%60:02d}'
                else:
                    eta_str = '--:--'
                
                status = f'Speed: {speed_str} | ETA: {eta_str}'
                self.progress.emit(percentage, status)
                
            except Exception as e:
                self.progress.emit(0, str(e))
        elif d['status'] == 'error':
            self.error.emit(str(d.get('error', 'Unknown error')))

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def sanitize_filename(self, filename):
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def get_safe_filename(self, title, ext):
        # Create a safe filename from the video title
        base_filename = self.sanitize_filename(title)
        filename = f"{base_filename}.{ext}"
        
        # If file exists, add a number to the end
        counter = 1
        while os.path.exists(os.path.join(self.save_path, filename)):
            filename = f"{base_filename} ({counter}).{ext}"
            counter += 1
            
        return filename

    def run(self):
        try:
            # Get video title and extension
            title = self.video_info.get('title', 'video')
            format_info = next((f for f in self.video_info['formats'] 
                              if f['format_id'] == self.format_id), None)
            
            if not format_info:
                self.error.emit("Selected format not found")
                return
                
            ext = format_info.get('ext', 'mp4')
            
            # Get safe filename
            filename = self.get_safe_filename(title, ext)
            
            ydl_opts = {
                'format': self.format_id,
                'progress_hooks': [self.progress_hook],
                'outtmpl': os.path.join(self.save_path, filename),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class NotificationWidget(QWidget):
    closed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setParent(None)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 200)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header with icon
        header_layout = QHBoxLayout()
        
        # Success icon
        icon_label = QLabel()
        success_icon = create_svg_icon("""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path fill="#4CAF50" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
            </svg>
        """, QSize(32, 32))
        icon_label.setPixmap(success_icon)
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel("Download Complete!")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Close button
        close_button = QPushButton("×")
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #aaa;
                font-size: 20px;
                font-weight: bold;
                padding: 5px;
                min-width: 30px;
            }
            QPushButton:hover {
                background: transparent;
                color: white;
            }
        """)
        close_button.clicked.connect(self.close)
        header_layout.addWidget(close_button)
        
        layout.addLayout(header_layout)
        
        # Message
        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.message_label)
        
        # Spacer
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setIcon(QIcon(create_svg_icon(LOCATION_ICON, QSize(16, 16))))
        button_layout.addWidget(self.open_folder_btn)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.close)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
        
        # Auto-close timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.setSingleShot(True)

    def show_notification(self, message, folder_path, callback):
        self.message_label.setText(message)
        self.open_folder_btn.clicked.connect(callback)
        
        # Position in bottom right
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.width() - self.width() - 20,
            screen.height() - self.height() - 40
        )
        
        self.show()
        self.timer.start(10000)  # Auto-close after 10 seconds

    def closeEvent(self, event):
        self.hide()
        self.closed.emit()
        event.accept()

class TubeMasterPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TubeMaster Pro - CODED BY TELVIN TEUM")
        self.setMinimumSize(1000, 800)
        
        # Initialize variables first
        self.video_info = None
        self.is_searching = False
        self.search_worker = None
        self.notification = None  # Store notification reference
        
        # Set default download directory
        self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "TubeMaster")
        
        # Then setup UI
        self.setup_ui()
        
        # Create loading overlay last
        self.loading_overlay = LoadingOverlay(self)
        
        # Set window background color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QComboBox {
                color: #ffffff;
                background-color: #3b3b3b;
            }
            QLineEdit {
                color: #ffffff;
                background-color: #3b3b3b;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Add title and credit
        title_layout = QVBoxLayout()
        title_label = QLabel("TubeMaster Pro")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        credit_label = QLabel("CODED BY TELVIN TEUM")
        credit_label.setStyleSheet("""
            font-size: 14px;
            color: #888888;
            margin-bottom: 20px;
        """)
        credit_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(credit_label)
        layout.addLayout(title_layout)

        # Search section
        search_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL...")
        self.url_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                border: 2px solid #555555;
                border-radius: 8px;
                font-size: 16px;
                min-width: 400px;
            }
            QLineEdit:focus {
                border-color: #FF0000;
            }
        """)
        
        self.search_button = QPushButton("Search")
        self.search_button.setIcon(QIcon(create_svg_icon(SEARCH_ICON, QSize(24, 24))))
        self.search_button.setStyleSheet("""
            QPushButton {
                padding: 15px 30px;
                background-color: #FF0000;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        self.search_button.clicked.connect(self.search_video)
        
        search_layout.addWidget(self.url_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Preview section
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(400)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #3b3b3b;
                border: 2px solid #555555;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.preview_label)

        # Video info
        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)

        # Download options section
        download_section = QFrame()
        download_section.setStyleSheet("""
            QFrame {
                background-color: #3b3b3b;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        download_layout = QVBoxLayout(download_section)
        
        # Download location display
        location_header = QHBoxLayout()
        location_label = QLabel("Download Location:")
        location_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        self.current_location_label = QLabel()
        self.current_location_label.setStyleSheet("""
            QLabel {
                color: #aaaaaa;
                padding: 5px 10px;
                background-color: #2b2b2b;
                border-radius: 5px;
            }
        """)
        self.update_location_label()
        
        location_header.addWidget(location_label)
        location_header.addWidget(self.current_location_label, 1)
        download_layout.addLayout(location_header)
        
        # Format and buttons
        controls_layout = QHBoxLayout()
        
        # Format selection
        self.format_combo = QComboBox()
        self.format_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 2px solid #555555;
                border-radius: 8px;
                min-width: 300px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #3b3b3b;
                color: white;
                selection-background-color: #555555;
            }
        """)
        
        # Download location button
        self.location_button = QPushButton("Change Location")
        self.location_button.setIcon(QIcon(create_svg_icon(LOCATION_ICON, QSize(24, 24))))
        self.location_button.setStyleSheet("""
            QPushButton {
                padding: 12px 20px;
                background-color: #666666;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        self.location_button.clicked.connect(self.change_download_location)
        
        # Download button
        self.download_button = QPushButton("Download")
        self.download_button.setIcon(QIcon(create_svg_icon(DOWNLOAD_ICON, QSize(24, 24))))
        self.download_button.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
        """)
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setEnabled(False)
        
        controls_layout.addWidget(self.format_combo)
        controls_layout.addWidget(self.location_button)
        controls_layout.addWidget(self.download_button)
        download_layout.addLayout(controls_layout)
        
        layout.addWidget(download_section)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 8px;
                text-align: center;
                height: 30px;
                font-size: 14px;
                font-weight: bold;
                background-color: #3b3b3b;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)

    def show_loading(self, show=True):
        if show:
            self.loading_overlay.resize(self.size())
            self.loading_overlay.progress.setValue(0)
            self.loading_overlay.show()
            self.url_input.setEnabled(False)
            self.search_button.setEnabled(False)
            self.is_searching = True
        else:
            self.loading_overlay.hide()
            self.url_input.setEnabled(True)
            self.search_button.setEnabled(True)
            self.is_searching = False

    def search_video(self):
        if self.is_searching:
            return
            
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL")
            return

        self.show_loading(True)
        self.download_button.setEnabled(False)
        self.format_combo.clear()
        self.preview_label.clear()
        self.title_label.clear()
        
        self.search_worker = SearchWorker(url)
        self.search_worker.progress.connect(self.loading_overlay.set_progress)
        self.search_worker.finished.connect(self.handle_search_complete)
        self.search_worker.error.connect(self.handle_search_error)
        self.search_worker.start()

    def handle_search_complete(self, result):
        try:
            self.video_info = result['info']
            
            # Update thumbnail
            if result['thumbnail']:
                pixmap = QPixmap()
                pixmap.loadFromData(result['thumbnail'])
                self.preview_label.setPixmap(pixmap)

            # Update title
            self.title_label.setText(self.video_info.get('title', ''))

            # Update formats
            formats = self.video_info.get('formats', [])
            
            # Add video+audio formats
            for f in formats:
                if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    format_str = f"Video+Audio - {f.get('ext', 'N/A')} - {f.get('format_note', 'N/A')}"
                    if f.get('filesize'):
                        format_str += f" ({self.format_size(f.get('filesize'))})"
                    self.format_combo.addItem(format_str, f.get('format_id'))
            
            # Add audio-only formats
            for f in formats:
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    format_str = f"Audio Only - {f.get('ext', 'N/A')} - {f.get('format_note', 'N/A')}"
                    if f.get('filesize'):
                        format_str += f" ({self.format_size(f.get('filesize'))})"
                    self.format_combo.addItem(format_str, f.get('format_id'))

            self.download_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing video info: {str(e)}")
        finally:
            self.show_loading(False)

    def handle_search_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"Error fetching video info: {error_msg}")
        self.show_loading(False)

    def update_location_label(self):
        # Ensure the download directory exists
        if not os.path.exists(self.download_dir):
            try:
                os.makedirs(self.download_dir)
            except Exception as e:
                QMessageBox.warning(self, "Warning", f"Could not create download directory: {str(e)}")
        
        # Update the label with the current location
        home = os.path.expanduser("~")
        display_path = self.download_dir.replace(home, "~")
        self.current_location_label.setText(display_path)
        self.current_location_label.setToolTip(self.download_dir)

    def change_download_location(self):
        new_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Download Directory",
            self.download_dir,
            QFileDialog.ShowDirsOnly
        )
        if new_dir:
            self.download_dir = new_dir
            self.update_location_label()

    def start_download(self):
        if not self.video_info:
            return

        # Ensure download directory exists
        if not os.path.exists(self.download_dir):
            try:
                os.makedirs(self.download_dir)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create download directory: {str(e)}")
                return

        format_id = self.format_combo.currentData()
        
        # Create download worker with video info
        self.download_worker = DownloadWorker(
            self.url_input.text(),
            format_id,
            self.download_dir,
            self.video_info
        )
        
        self.download_worker.progress.connect(self.update_progress)
        self.download_worker.finished.connect(self.download_finished)
        self.download_worker.error.connect(self.download_error)
        
        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.download_worker.start()

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def update_progress(self, percentage, status):
        self.progress_bar.setValue(int(percentage))
        self.progress_bar.setFormat(f"{percentage:.1f}% | {status}")

    def download_finished(self):
        self.download_button.setEnabled(True)
        self.progress_bar.setValue(100)
        
        # Clean up previous notification if it exists
        if self.notification:
            self.notification.close()
            self.notification = None
        
        # Create and show new notification
        self.notification = NotificationWidget()
        self.notification.closed.connect(self._on_notification_closed)
        message = f"Video has been downloaded successfully!\nLocation: {self.download_dir}"
        self.notification.show_notification(message, self.download_dir, self.open_download_folder)

    def _on_notification_closed(self):
        self.notification = None

    def open_download_folder(self):
        try:
            if sys.platform == 'win32':
                os.startfile(self.download_dir)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{self.download_dir}"')
            else:  # Linux
                try:
                    os.system(f'xdg-open "{self.download_dir}"')
                except:
                    # Fallback to common file managers
                    for file_manager in ['nautilus', 'dolphin', 'thunar', 'pcmanfm', 'nemo']:
                        try:
                            os.system(f'{file_manager} "{self.download_dir}"')
                            break
                        except:
                            continue
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not open folder: {str(e)}\nPath: {self.download_dir}")

    def download_error(self, error_msg):
        self.download_button.setEnabled(True)
        QMessageBox.critical(self, "Download Error", str(error_msg))

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application-wide stylesheet
    app.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QMessageBox QPushButton {
            padding: 8px 16px;
            border-radius: 4px;
            background-color: #4CAF50;
            color: white;
            border: none;
            min-width: 100px;
        }
        QMessageBox QPushButton:hover {
            background-color: #45a049;
        }
    """)
    
    window = TubeMasterPro()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
