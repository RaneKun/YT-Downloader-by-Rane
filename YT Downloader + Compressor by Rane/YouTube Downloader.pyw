# Import necessary classes from PyQt6 for creating the GUI
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
    QCheckBox, QTextEdit, QLabel, QProgressBar, QFileDialog, QScrollArea, QDialog, QSizePolicy
)
# QApplication: Manages application control flow and main settings
# QMainWindow: Provides a main application window
# QWidget: Base class for all UI objects
# QVBoxLayout: Lines up widgets vertically
# QHBoxLayout: Lines up widgets horizontally
# QPushButton: Creates clickable buttons
# QFrame: Provides a container widget that can be styled
# QCheckBox: Creates toggleable checkboxes
# QTextEdit: Provides multi-line text editing
# QLabel: Displays text or images
# QProgressBar: Shows progress of an operation
# QFileDialog: Provides dialog for file selection
# QScrollArea: Provides a scrolling view
# QDialog: Creates dialog windows
# QSizePolicy: Controls layout behavior

# Import QPixmap for handling images, QIcon for window icons and QFont to display custom font
from PyQt6.QtGui import QPixmap, QIcon, QFont
# QPixmap: Handles images for display
# QIcon: Provides scalable icons
# QFont: Specifies font for text rendering

# Import core classes for threading and signals
from PyQt6.QtCore import Qt, QThread, pyqtSignal
# Qt: Contains core Qt enums and flags
# QThread: Provides platform-independent threads
# pyqtSignal: Creates signals for communication between objects

import sys  # Provides access to command line arguments and system functions
import subprocess  # Allows running external commands
import os  # Provides operating system dependent functionality
import re  # Provides regular expression operations
import shutil  # Provides high-level file operations
import yt_dlp  # Provides YouTube downloading capabilities
import requests  # Provides HTTP request functionality
import importlib.util # Provides tools for dynamic module loading
import datetime  # Provides date and time functionality
from io import BytesIO  # Provides in-memory byte stream handling

# Main application class for the YouTube Downloader
class YouTubeDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()  # Initialize the parent QMainWindow class
        print("[INIT] Initializing YouTubeDownloaderApp main window...")  # Debug: Main window initialization
        self.setWindowTitle("YouTube Downloader by Rane")  # Set window title
        self.setWindowIcon(QIcon('Main Files/Assests/YouTube Downloader/default_icon.ico'))  # Set window icon
        self.worker = None  # Initialize worker thread reference to None
        self.total_tasks = 0  # Initialize total download tasks counter
        self.completed_tasks = 0  # Initialize completed tasks counter
        self.output_dir = self.load_last_output_dir()  # Load last used output directory
        print(f"[CONFIG] Loaded output directory: {self.output_dir}")  # Debug: Output directory loaded
        self.init_ui()  # Initialize user interface
        print("[INIT] YouTubeDownloaderApp initialization complete")  # Debug: Main window ready

    def init_ui(self):
        print("[UI] Initializing user interface components...")  # Debug: UI setup starting
        # Set the Window Scale and also center it
        self.resize(725, 725)  # Set initial window size
        self.setMinimumSize(725, 725)  # Set minimum window size
        self.center_window()  # Center window on screen

        #Initialize various UI components
        self.init_background()  # Set up window background
        self.init_layouts()  # Create layout structures
        self.init_url_input()  # Set up URL input field
        self.init_link_counter()  # Set up link counter
        self.init_preview_button()  # Set up preview button
        self.init_checkboxes()  # Set up download option checkboxes
        self.init_output_selection()  # Set up output directory selection
        self.init_action_buttons()  # Set up action buttons
        self.init_progress_status()  # Set up progress indicators
        self.init_central_widget()  # Set up central widget container

        self.update_button_states(downloading=False)  # Set initial button states
        print("[UI] User interface initialization complete")  # Debug: UI fully set up

    def init_background(self):
        print("[UI] Setting up background image...")  # Debug: Background setup
        self.background_label = QLabel(self)  # Create label for background
        self.set_background_image('Main Files/Assests/YouTube Downloader/default_background.jpg')  # Load background image
        print("[UI] Background setup complete")  # Debug: Background ready

    def init_layouts(self):
        print("[UI] Creating layout structures...")  # Debug: Layout creation
        main_layout = QVBoxLayout()  # Main vertical layout
        checkbox_layout = QHBoxLayout()  # Horizontal layout for checkboxes
        button_layout = QHBoxLayout()  # Horizontal layout for buttons
        output_layout = QHBoxLayout()  # Horizontal layout for output selection
        self.main_layout = main_layout  # Store main layout reference
        self.checkbox_layout = checkbox_layout  # Store checkbox layout reference
        self.button_layout = button_layout  # Store button layout reference
        self.output_layout = output_layout  # Store output layout reference
        print("[UI] Layout structures created")  # Debug: Layouts ready

    def init_url_input(self):
        print("[UI] Configuring URL input field...")  # Debug: URL input setup
        self.url_input = QTextEdit()  # Create text edit for URLs
        self.url_input.setPlaceholderText("Paste YouTube links here... (One per line)")  # Set placeholder text
        self.url_input.setStyleSheet("background-color: rgba(255, 255, 255, 25); color: blue; font-size: 14px;")  # Set styling
        self.url_input.textChanged.connect(self.update_link_count)  # Connect text change signal
        self.main_layout.addWidget(self.url_input)  # Add to main layout
        print("[UI] URL input field configured")  # Debug: URL input ready

    def init_link_counter(self):
        print("[UI] Setting up link counter...")  # Debug: Link counter setup
        self.link_count_label = QLabel("Links: 0")  # Create link counter label
        self.link_count_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)  # Set alignment
        self.main_layout.addWidget(self.link_count_label)  # Add to main layout
        print("[UI] Link counter ready")  # Debug: Link counter functional

    def init_preview_button(self):
        print("[UI] Configuring preview button...")  # Debug: Preview button setup
        self.preview_button = QPushButton("Preview Link(s) (UI will freeze! 🥶)")  # Create preview button
        self.preview_button.clicked.connect(self.open_preview_window)  # Connect click signal
        self.main_layout.addWidget(self.preview_button)  # Add to main layout
        print("[UI] Preview button configured")  # Debug: Preview button ready

    def init_checkboxes(self):
        print("[UI] Setting up download option checkboxes...")  # Debug: Checkbox setup
        self.download_video_checkbox = QCheckBox("Download Video️ 📽️")  # Video download checkbox
        self.download_audio_checkbox = QCheckBox("Download Audio 🔊")  # Audio download checkbox
        self.download_thumbnail_checkbox = QCheckBox("Download Thumbnail 🖼️")  # Thumbnail download checkbox

        # Connect stateChanged signals to debug functions
        self.download_video_checkbox.stateChanged.connect(self.debug_video_checkbox_changed)
        self.download_audio_checkbox.stateChanged.connect(self.debug_audio_checkbox_changed)
        self.download_thumbnail_checkbox.stateChanged.connect(self.debug_thumbnail_checkbox_changed)

        self.checkbox_layout.addWidget(self.download_video_checkbox)  # Add to checkbox layout
        self.checkbox_layout.addWidget(self.download_audio_checkbox)  # Add to checkbox layout
        self.checkbox_layout.addWidget(self.download_thumbnail_checkbox)  # Add to checkbox layout

        self.main_layout.addLayout(self.checkbox_layout)  # Add checkbox layout to main
        print("[UI] Download option checkboxes ready")  # Debug: Checkboxes functional

    def init_output_selection(self):
        print("[UI] Configuring output directory selection...")  # Debug: Output selection setup
        self.output_label = QLabel(f"Selected output folder: {self.output_dir}")  # Output directory label
        self.browse_button = QPushButton("Browse Output Folder 📁")  # Browse button
        self.browse_button.clicked.connect(self.select_output_folder)  # Connect click signal

        self.open_folder_button = QPushButton("Open Output Folder 📂")  # Open folder button
        self.open_folder_button.clicked.connect(self.open_output_folder)  # Connect click signal

        self.output_layout.addWidget(self.output_label)  # Add to output layout
        self.output_layout.addWidget(self.browse_button)  # Add to output layout
        self.output_layout.addWidget(self.open_folder_button)  # Add to output layout
        self.main_layout.addLayout(self.output_layout)  # Add to main layout
        print("[UI] Output directory selection configured")  # Debug: Output selection ready

    def init_action_buttons(self):
        print("[UI] Setting up action buttons...")  # Debug: Action buttons setup
        self.start_button = QPushButton("Start ⚡")  # Start download button
        self.start_button.clicked.connect(self.start_download)  # Connect click signal
        self.update_button = QPushButton("Check for yt-dlp update 🕹️")  # Update button
        self.update_button.clicked.connect(self.check_yt_dlp_update)  # Connect click signal
        self.load_cookie_button = QPushButton("Load Cookie File 🍪(optional)")  # Cookie button
        self.load_cookie_button.clicked.connect(self.load_cookie_file)  # Connect click signal

        self.button_layout.addWidget(self.load_cookie_button)  # Add to button layout
        self.button_layout.addWidget(self.start_button)  # Add to button layout
        self.button_layout.addWidget(self.update_button)  # Add to button layout
        self.main_layout.addLayout(self.button_layout)  # Add to main layout
        print("[UI] Action buttons configured")  # Debug: Action buttons ready

    def init_progress_status(self):
        print("[UI] Setting up progress indicators...")  # Debug: Progress UI setup
        self.progress_bar = QProgressBar()  # Create progress bar
        self.progress_bar.setMaximum(100)  # Set maximum value
        self.progress_bar.setValue(0)  # Initialize value
        self.main_layout.addWidget(self.progress_bar)  # Add to main layout

        self.remaining_files_label = QLabel("Remaining files: 0")  # Remaining files label
        self.main_layout.addWidget(self.remaining_files_label)  # Add to main layout

        self.speed_label = QLabel("Status: Idle (buttons will remain non-clickable and ui will remain non-scalable till download completes, please be patient) ✌️")  # Status label
        self.main_layout.addWidget(self.speed_label)  # Add to main layout
        print("[UI] Progress indicators ready")  # Debug: Progress UI functional

    def init_central_widget(self):
        print("[UI] Creating central widget container...")  # Debug: Central widget setup
        central_widget = QWidget()  # Create central widget
        central_widget.setLayout(self.main_layout)  # Set main layout
        self.setCentralWidget(central_widget)  # Set as central widget
        print("[UI] Central widget ready")  # Debug: Main container complete

    def center_window(self):
        print("[WINDOW] Calculating window center position...")  # Debug: Window positioning
        screen_geometry = QApplication.primaryScreen().geometry()  # Get screen dimensions
        x = (screen_geometry.width() - self.width()) // 2  # Calculate x position
        y = (screen_geometry.height() - self.height()) // 2  # Calculate y position
        self.move(x, y)  # Move window to center
        print("[WINDOW] Window centered on screen")  # Debug: Positioning complete

    def set_background_image(self, image_path):
        print(f"[UI] Loading background image from: {image_path}")  # Debug: Background image load
        self.background_pixmap = QPixmap(image_path)  # Load image into pixmap
        self.update_background()  # Update background display
        print("[UI] Background image loaded and applied")  # Debug: Background ready

    def update_background(self):
        print("[UI] Updating background scaling...")  # Debug: Background scaling
        if hasattr(self, 'background_pixmap'):  # Check if pixmap exists
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),  # Scale to window size
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,  # Keep aspect ratio
                Qt.TransformationMode.SmoothTransformation  # Smooth scaling
            )  # Create scaled pixmap
            self.background_label.setPixmap(scaled_pixmap)  # Set scaled pixmap
            self.background_label.setGeometry(0, 0, self.width(), self.height())  # Set geometry
            self.background_label.lower()  # Move to background
        print("[UI] Background scaling updated")  # Debug: Scaling complete

    def resizeEvent(self, event):
        print("[WINDOW] Handling window resize event...")  # Debug: Resize event
        super().resizeEvent(event)  # Call parent class handler
        self.update_background()  # Update background
        print("[WINDOW] Resize handled, background updated")  # Debug: Resize complete

    def update_link_count(self):
        print("[URL] Updating link counter...")  # Debug: Link count update
        urls = self.url_input.toPlainText().strip().splitlines()  # Get URLs from text
        urls = [url.strip() for url in urls if url.strip()]  # Clean URLs
        self.link_count_label.setText(f"Links: {len(urls)}")  # Update count
        print(f"[URL] Current link count: {len(urls)}")  # Debug: Count updated

    def open_output_folder(self):
        print(f"[FOLDER] Attempting to open output folder: {self.output_dir}")  # Debug: Folder open attempt
        if os.path.exists(self.output_dir):  # Check if directory exists
            os.startfile(self.output_dir)  # Open folder
            print("[FOLDER] Output folder opened successfully")  # Debug: Folder opened
        else:
            print(f"[ERROR] Output folder does not exist: {self.output_dir}")  # Debug: Missing folder

    def select_output_folder(self):
        print("[FOLDER] Opening folder selection dialog...")  # Debug: Folder selection
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")  # Open dialog
        if folder:  # If folder selected
            self.output_dir = folder  # Set output directory
            self.output_label.setText(f"Selected output folder: {self.output_dir}")  # Update label
            self.save_output_dir()  # Save directory
            print(f"[FOLDER] Selected output folder: {self.output_dir}")  # Debug: Folder selected
        else:
            print("[FOLDER] Folder selection cancelled by user")  # Debug: Selection cancelled

    def load_last_output_dir(self):
        print("[CONFIG] Attempting to load last used output directory...")  # Debug: Config load attempt
        try:
            with open("Main Files/Configs/YouTube Downloader/output directory.txt", "r") as file:  # Open config file
                directory = file.read().strip()  # Read directory path
                if os.path.exists(directory):  # Check if directory exists
                    print(f"[CONFIG] Found valid output directory: {directory}")  # Debug: Config loaded
                    return directory  # Return directory
        except FileNotFoundError:  # If file doesn't exist
            print("[CONFIG] No output directory config found, using default")  # Debug: Using default
            pass  # Continue
        default_dir = os.path.abspath("Output 📤")  # Default directory
        print(f"[CONFIG] Using default output directory: {default_dir}")  # Debug: Default directory set
        return default_dir

    def save_output_dir(self):
        print(f"[CONFIG] Saving current output directory: {self.output_dir}")  # Debug: Saving config
        os.makedirs("Main Files/Configs/YouTube Downloader", exist_ok=True)  # Create config dir
        with open("Main Files/Configs/YouTube Downloader/output directory.txt", "w") as file:  # Open file
            file.write(self.output_dir)  # Write directory
        print("[CONFIG] Output directory saved successfully")  # Debug: Config saved

    def load_cookie_file(self):
        """Opens a file dialog to select 'www.youtube.com_cookies.txt' and copies it to the specified directory."""
        print("[COOKIE] Starting cookie file load process...")  # Debug: Cookie load start
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cookie File", "", "www.youtube.com_cookies (*.txt)")  # Open dialog
        print(f"[COOKIE] Selected file path: {file_path}")  # Debug: File selected

        if file_path:  # If file selected
            if os.path.basename(file_path) == "www.youtube.com_cookies.txt":  # Check filename
                cookie_option = r'Main Files/Configs/YouTube Downloader/www.youtube.com_cookies.txt'  # Destination path
                try:
                    print(f"[COOKIE] Copying cookie file to: {cookie_option}")  # Debug: File copy
                    shutil.copyfile(file_path, cookie_option)  # Copy file
                    self.speed_label.setText("Cookie file loaded successfully! 👍")  # Update status
                    print("[COOKIE] Cookie file loaded successfully")  # Debug: Load success
                except Exception as e:
                    error_message = f"Error copying cookie file: {str(e)}"
                    self.speed_label.setText(error_message)  # Show error
                    print(f"[ERROR] Cookie file copy failed: {error_message}")  # Debug: Copy failed
            else:
                error_message = "Error: Invalid cookie file name. Please select 'www.youtube.com_cookies.txt'"
                self.speed_label.setText(error_message)  # Show error
                print(f"[ERROR] {error_message}")  # Debug: Invalid filename
        else:
            print("[COOKIE] Cookie file selection cancelled")  # Debug: Selection cancelled

    def open_preview_window(self):
            print("[PREVIEW] Opening link preview window...")  # Debug: Preview initiation

            # Get URLs from input field
            urls = self.url_input.toPlainText().strip().splitlines()
            urls = [url.strip() for url in urls if url.strip()]  # Clean URLs
            print(f"[PREVIEW] URLs to preview: {urls}") # Debug: URL list

            # Check if any URLs provided
            if not urls:
                self.speed_label.setText("Error: No URLs provided to preview 😐")  # Show error
                print("[ERROR] Preview aborted - no URLs provided")  # Debug: Missing URLs
                return  # Exit

            # Define cookie file path
            cookie_option = r'Main Files/Configs/YouTube Downloader/www.youtube.com_cookies.txt'

            # Create preview dialog window
            preview_window = QDialog(self)
            preview_window.setWindowTitle("Link Preview(s) 🔗")  # Set title
            preview_window.setGeometry(0, 0, 1100, 725)  # Set size
            qr = preview_window.frameGeometry() # Get window geometry
            cp = self.screen().availableGeometry().center() # Get screen center
            qr.moveCenter(cp) # Center window
            preview_window.move(qr.topLeft())  # Move to center
            print("[PREVIEW] Window geometry set and centered") # Debug: Window positioning
            layout = QVBoxLayout()  # Create layout

            # Create scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)  # Allow resizing
            scroll_content = QWidget()  # Scroll content
            self.preview_layout = QVBoxLayout(scroll_content)  # Content layout
            scroll_area.setWidget(scroll_content)  # Set content
            print("[PREVIEW] Scroll area created") # Debug: Scroll setup

            layout.addWidget(scroll_area)  # Add scroll to layout
            preview_window.setLayout(layout)  # Set window layout
            print("[PREVIEW] Layout configured") # Debug: Layout ready

            # yt-dlp options
            ydl_opts = {
                'quiet': True,  # Suppress output
                'no_warnings': True,  # Suppress warnings
                'cookiefile': cookie_option  # Use cookies
            }
            print(f"[PREVIEW] yt-dlp options configured with cookie file: {cookie_option}")  # Debug: Options set

            # Process each URL
            for url in urls:
                print(f"[PREVIEW] Processing URL: {url}") # Debug: URL processing
                try:
                    # Get video info
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        print("[PREVIEW] yt-dlp instance created") # Debug: Extractor ready
                        info_dict = ydl.extract_info(url, download=False)  # Get info
                        print("[PREVIEW] Video information extracted") # Debug: Info retrieved
                        if info_dict:  # If info received
                            print("[PREVIEW] Valid video information received") # Debug: Info valid
                            # Create preview frame
                            preview_frame = QFrame()
                            preview_frame_layout = QHBoxLayout(preview_frame)  # Horizontal layout
                            preview_frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: #f0f0f0;")  # Style
                            print("[PREVIEW] Preview frame created") # Debug: Frame ready

                            # Add title label
                            title_label = QLabel(info_dict.get('title', 'No Title'))  # Get title
                            title_label.setWordWrap(True)  # Allow wrapping
                            title_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #555;")  # Style
                            preview_frame_layout.addWidget(title_label, 2)  # Add to layout
                            print("[PREVIEW] Title label added") # Debug: Title shown

                            # Add artist label
                            artist_name = info_dict.get('artist') or info_dict.get('uploader') or 'Unknown Artist' # Get artist
                            artist_label = QLabel(f"{artist_name}") # Create label
                            artist_label.setWordWrap(True) # Allow wrapping
                            artist_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #555;")  # Style
                            preview_frame_layout.addWidget(artist_label, 2) # Add to layout
                            print("[PREVIEW] Artist label added") # Debug: Artist shown

                            # Add thumbnail if available
                            thumbnail_url = info_dict.get('thumbnail')
                            if thumbnail_url:  # If thumbnail exists
                                print("[PREVIEW] Thumbnail URL found") # Debug: Thumbnail available
                                try:
                                    # Download thumbnail
                                    image_data = requests.get(thumbnail_url).content
                                    print("[PREVIEW] Thumbnail downloaded") # Debug: Image fetched
                                    pixmap = QPixmap()  # Create pixmap
                                    pixmap.loadFromData(image_data)  # Load image
                                    print("[PREVIEW] Thumbnail loaded into QPixmap") # Debug: Image loaded
                                    pixmap = pixmap.scaled(480, 270, Qt.AspectRatioMode.KeepAspectRatio)  # Scale
                                    thumbnail_label = QLabel()  # Create label
                                    thumbnail_label.setPixmap(pixmap)  # Set image
                                    preview_frame_layout.addWidget(thumbnail_label, 1)  # Add to layout
                                    print("[PREVIEW] Thumbnail added to preview") # Debug: Thumbnail shown

                                except Exception as e:
                                    print(f"[ERROR] Thumbnail load failed: {e}")  # Debug: Thumbnail error
                                    thumbnail_label = QLabel("Thumbnail Unavailable")  # Fallback
                                    preview_frame_layout.addWidget(thumbnail_label, 1)  # Add to layout
                                    print("[PREVIEW] Thumbnail placeholder shown") # Debug: Fallback used
                            else:
                                thumbnail_label = QLabel("No Thumbnail")  # Fallback
                                preview_frame_layout.addWidget(thumbnail_label, 1)  # Add to layout
                                print("[PREVIEW] No thumbnail available") # Debug: No thumbnail

                            # Add frame to layout
                            self.preview_layout.addWidget(preview_frame)
                            print("[PREVIEW] Preview frame added to layout") # Debug: Frame added

                except Exception as e:
                    # Handle errors
                    error_label = QLabel(f"(might wanna use cookies 🍪) Error fetching info for {url}: {e}")  # Error label
                    error_label.setStyleSheet("color: red;")  # Style
                    self.preview_layout.addWidget(error_label)  # Add to layout
                    print(f"[ERROR] URL preview failed for {url}: {e}") # Debug: Preview error

            # Show preview window
            preview_window.exec()
            print("[PREVIEW] Window closed")  # Debug: Preview complete

    def check_yt_dlp_update(self):
        """Check how yt-dlp was installed and update it accordingly."""
        print("[UPDATE] Checking yt-dlp installation method...")  # Debug: Update check
        # Check if yt-dlp is a pip package
        yt_dlp_spec = importlib.util.find_spec("yt_dlp")
        if yt_dlp_spec and yt_dlp_spec.origin and "site-packages" in yt_dlp_spec.origin:
            # Installed via pip
            update_command = ["cmd", "/c", "start", "cmd", "/k", "pip install --upgrade yt-dlp"]
            print("[UPDATE] yt-dlp installed via pip, using pip upgrade")  # Debug: Pip update
        else:
            # Installed as a standalone binary
            update_command = ["cmd", "/c", "start", "cmd", "/k", "yt-dlp -U"]
            print("[UPDATE] yt-dlp installed as binary, using built-in updater")  # Debug: Binary update

        print(f"[UPDATE] Executing update command: {update_command}")  # Debug: Command execution
        subprocess.Popen(update_command)  # Execute update
        print("[UPDATE] Update process started")  # Debug: Update initiated

    def start_download(self):
        print("[DOWNLOAD] Starting download process...")  # Debug: Download initiation
        if self.worker and self.worker.isRunning:  # Check if already downloading
            self.speed_label.setText("Download already in progress 😑")  # Show message
            print("[WARNING] Download start aborted - already in progress")  # Debug: Duplicate start
            return  # Exit

        # Reset error list
        self.download_errors = []

        # Reset worker if exists
        if self.worker: # Check existing worker
            print("[WORKER] Stopping previous worker thread...")  # Debug: Worker cleanup
            self.worker.quit() # Stop worker
            self.worker.wait() # Wait for stop
            self.worker = None # Reset reference
            print("[WORKER] Previous worker stopped")  # Debug: Cleanup complete

        # Get URLs from input
        urls = self.url_input.toPlainText().strip().splitlines()
        urls = [url.strip() for url in urls if url.strip()]  # Clean URLs

        if not urls:  # If no URLs
            self.speed_label.setText("Error: No URLs provided 🫥")  # Show error
            print("[ERROR] Download start aborted - no URLs provided")  # Debug: Missing URLs
            return  # Exit

        # Create download tasks based on checkboxes
        tasks = []  # Initialize tasks list
        if self.download_video_checkbox.isChecked():  # If video selected
            tasks.append({"type": "video", "urls": urls.copy()})  # Add video task
        if self.download_audio_checkbox.isChecked():  # If audio selected
            tasks.append({"type": "audio", "urls": urls.copy()})  # Add audio task
        if self.download_thumbnail_checkbox.isChecked():  # If thumbnail selected
            tasks.append({"type": "thumbnail", "urls": urls.copy()})  # Add thumbnail task

        if not tasks:  # If no tasks
            self.speed_label.setText("Error: Select at least one download option 🙄")  # Show error
            print("[ERROR] Download start aborted - no download options selected")  # Debug: No options
            return  # Exit

        # Calculate total tasks
        self.total_tasks = 0 # Reset counter
        for task in tasks:
            self.total_tasks += len(task["urls"]) # Sum all URLs
        self.completed_tasks = 0  # Reset completed
        self.update_button_states(downloading=True)  # Update UI state
        self.remaining_files_label.setText(f"Remaining files: {self.total_tasks}")  # Update label
        self.setFixedSize(self.size()) # Prevent UI resizing
        print(f"[DOWNLOAD] Starting {self.total_tasks} download tasks")  # Debug: Task count
        self.process_tasks(tasks)  # Start processing

    def process_tasks(self, tasks):
        print(f"[TASK] Processing task queue (remaining tasks: {len(tasks)})")  # Debug: Task processing
        if not tasks:  # If no more tasks
            print("[TASK] All tasks completed")  # Debug: Task queue empty
            self.on_all_tasks_finished()  # Handle completion
            return  # Exit

        current_task = tasks.pop(0)  # Get next task
        self.worker = DownloadWorker(current_task['type'], current_task['urls'], self.output_dir)  # Create worker
        self.worker.progress_signal.connect(self.progress_bar.setValue)  # Connect progress
        self.worker.speed_signal.connect(self.speed_label.setText)  # Connect speed
        self.worker.file_moved_signal.connect(self.update_remaining_files)  # Connect file moved
        self.worker.error_signal.connect(self.display_error)  # Connect errors
        self.worker.finished_signal.connect(lambda: self.process_tasks(tasks))  # Connect finished
        print(f"[WORKER] Starting worker for {current_task['type']} downloads")  # Debug: Worker start
        self.worker.start()  # Start worker

    def display_error(self, error_message):
        """Display yt-dlp errors in the UI and store them for the log file."""
        print(f"[ERROR] Download error encountered: {error_message}")  # Debug: Error captured
        if not hasattr(self, "download_errors"):
            self.download_errors = []  # Create error list if needed

        self.download_errors.append(error_message)  # Store error
        self.speed_label.setText(error_message)  # Show error in UI

    def export_error_log(self):
        """Save all download errors into a log file."""
        print("[LOG] Exporting error log...")  # Debug: Error logging
        log_file_path = os.path.join(os.getcwd(), "error-log 📃.txt")  # Log path

        with open(log_file_path, "a", encoding="utf-8") as log_file:  # Open log file
            log_file.write("\n" + "="*50 + "\n")  # Separator
            log_file.write(f"📅 Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")  # Timestamp
            log_file.write("⚠️ Errors encountered during downloads:\n")  # Header

            for error in self.download_errors:  # Write each error
                log_file.write(f"- {error}\n")  # Write error

            log_file.write("="*50 + "\n")  # Ending separator
        print(f"[LOG] Errors saved to {log_file_path}")  # Debug: Log saved

    # Debugging functions for checkbox state changes
    def debug_video_checkbox_changed(self, state):
        # Check if checkbox is checked (state == 2)
        if state == 2:
            print("[CHECKBOX] Video download option selected")  # Debug: Selected
        else:
            print("[CHECKBOX] Video download option deselected")  # Debug: Deselected

    def debug_audio_checkbox_changed(self, state):
        # Check if checkbox is checked (state == 2)
        if state == 2:
            print("[CHECKBOX] Audio download option selected")  # Debug: Selected
        else:
            print("[CHECKBOX] Audio download option deselected")  # Debug: Deselected

    def debug_thumbnail_checkbox_changed(self, state):
        # Check if checkbox is checked (state == 2)
        if state == 2:
            print("[CHECKBOX] Thumbnail download option selected")  # Debug: Selected
        else:
            print("[CHECKBOX] Thumbnail download option deselected")  # Debug: Deselected

    def update_remaining_files(self):
        """Updates the remaining files counter and checks for completion."""
        self.completed_tasks += 1  # Increment completed
        remaining_files = self.total_tasks - self.completed_tasks  # Calculate remaining
        self.remaining_files_label.setText(f"Remaining files: {remaining_files}")  # Update label
        print(f"[PROGRESS] File completed. Remaining: {remaining_files}")  # Debug: Progress
        if remaining_files == 0:  # If all done
            self.on_all_tasks_finished()  # Handle completion

    def on_all_tasks_finished(self):
        print("[DOWNLOAD] All download tasks completed")  # Debug: Download complete
        self.progress_bar.setValue(100)  # Set progress to 100%

        # Check for errors
        if hasattr(self, "download_errors") and self.download_errors:  # If errors
            self.speed_label.setText("The task is complete... but with error(s) ❌️ check log file (root directory) for details 📃 [may just need a cookie 🍪]")  # Show message
            self.export_error_log()  # Export errors
        else:
            self.speed_label.setText("The task is complete ✅")  # Show success

        self.update_button_states(downloading=False)  # Update UI state

        if self.worker:  # Clean up worker
            print("[WORKER] Stopping worker thread...")  # Debug: Worker cleanup
            self.worker.quit()  # Stop worker
            self.worker.wait()  # Wait for stop
            self.worker = None  # Reset reference
            print("[WORKER] Worker thread stopped")  # Debug: Cleanup complete

        # Allow UI resizing again
        print("[WINDOW] Enabling window resizing with minimum size 725x725")  # Debug enabling resize
        self.setMinimumSize(725, 725)  # Set minimum size
        self.setMaximumSize(16777215, 16777215)  # Allow expanding
        print("[WINDOW] Window resize limits set to default Qt maximum")  # Debug max size set
        print("[DOWNLOAD] Download process fully completed")  # Debug: Process complete

    def update_button_states(self, downloading=False):
        print(f"[UI] Updating button states (downloading={downloading})...")  # Debug: Button state change
        self.start_button.setEnabled(not downloading)  # Toggle start button
        self.download_video_checkbox.setEnabled(not downloading)  # Toggle video checkbox
        self.download_audio_checkbox.setEnabled(not downloading)  # Toggle audio checkbox
        self.download_thumbnail_checkbox.setEnabled(not downloading)  # Toggle thumbnail checkbox
        self.browse_button.setEnabled(not downloading)  # Toggle browse button
        self.update_button.setEnabled(not downloading)  # Toggle update button
        self.preview_button.setEnabled(not downloading)  # Toggle preview button
        self.load_cookie_button.setEnabled(not downloading)  # Toggle cookie button
        print("[UI] Button states updated")  # Debug: States applied

    def closeEvent(self, event):
        """Ensure the worker thread is stopped before closing the application."""
        print("[APP] Application closing requested...")  # Debug: Shutdown start
        if self.worker and self.worker.isRunning():
            print("[WORKER] Stopping active worker thread...")  # Debug: Worker cleanup
            self.worker.quit()  # Stop worker
            self.worker.wait()  # Wait for stop
            print("[WORKER] Worker thread stopped")  # Debug: Cleanup complete
        event.accept()  # Close window
        print("[APP] Application closed")  # Debug: Shutdown complete


# Worker class for handling downloads in a separate thread
class DownloadWorker(QThread):
    progress_signal = pyqtSignal(int)  # Signal for progress percentage
    speed_signal = pyqtSignal(str)  # Signal for download speed
    file_moved_signal = pyqtSignal(str)  # Signal for file moved
    error_signal = pyqtSignal(str)  # Signal for errors
    finished_signal = pyqtSignal()  # Signal for completion

    def __init__(self, download_type, urls, output_dir):
        super().__init__()  # Initialize QThread
        print(f"[WORKER] Initializing DownloadWorker for {download_type} downloads")  # Debug: Worker creation
        self.download_type = download_type  # Download type (video/audio/thumbnail)
        self.urls = urls  # List of URLs
        self.output_dir = output_dir  # Output directory
        self.isRunning = True  # Running flag
        print(f"[WORKER] Initialized with: type={download_type}, output_dir={output_dir}")  # Debug: Worker ready

    def run(self):
        """Main method that runs in the thread to perform downloads."""
        print(f"[WORKER] Starting download thread for {self.download_type}")  # Debug: Thread start
        os.makedirs(self.output_dir, exist_ok=True)  # Create output dir
        print(f"[WORKER] Output directory verified: {self.output_dir}")  # Debug: Directory check
        for url in self.urls:  # Process each URL
            if not self.isRunning:  # Check if canceled
                print("[WORKER] Download canceled by user")  # Debug: Cancel detected
                break  # Exit loop

            temp_output_dir = self.get_temp_dir()  # Get temp dir

            # Clean temp directory
            if os.path.exists(temp_output_dir):
                print(f"[WORKER] Cleaning existing temp directory: {temp_output_dir}")  # Debug: Temp cleanup
                shutil.rmtree(temp_output_dir)  # Remove dir
            os.makedirs(temp_output_dir)  # Create dir
            print(f"[WORKER] Created temp directory: {temp_output_dir}")  # Debug: Temp ready

            # Get yt-dlp command
            command = self.get_yt_dlp_command(url, temp_output_dir)

            # Execute command
            self.execute_yt_dlp(command, temp_output_dir)

        self.finished_signal.emit()  # Signal completion
        print(f"[WORKER] Download thread completed for {self.download_type}")  # Debug: Thread complete

    def get_temp_dir(self):
        """Returns the correct temporary directory based on the download type."""
        if self.download_type == "video":
            temp_dir = os.path.join("C:\\Windows\\Temp", "YT video downloader by Rane 📽️")  # Video temp
        elif self.download_type == "audio":
            temp_dir = os.path.join("C:\\Windows\\Temp", "YT audio downloader by Rane 🔊")  # Audio temp
        elif self.download_type == "thumbnail":
            temp_dir = os.path.join("C:\\Windows\\Temp", "YT thumbnail downloader by Rane 🖼️")  # Thumbnail temp
        else:
            temp_dir = os.path.join("C:\\Windows\\Temp", "YT downloader by Rane")  # Default temp
        print(f"[WORKER] Using temp directory: {temp_dir}")  # Debug: Temp directory
        return temp_dir

    def get_yt_dlp_command(self, url, temp_output_dir):
        """Returns the appropriate yt-dlp command based on the download type."""
        base_command = [
            "yt-dlp",  # yt-dlp command
            "-o", os.path.join(temp_output_dir, "%(title)s.%(ext)s"),  # Output format
            url  # URL
        ]

        # Cookie option
        cookie_option = ['--cookies', r'Main Files/Configs/YouTube Downloader/www.youtube.com_cookies.txt']

        if self.download_type == "video":
            command = base_command + cookie_option + [
                "--embed-thumbnail", "--add-metadata", "--write-thumbnail",  # Video options
                "-f", "bestvideo+bestaudio", "--merge-output-format", "mp4"  # Format
            ]
        elif self.download_type == "audio":
            command = base_command + cookie_option + [
                "-f", "bestaudio", "--extract-audio",  # Audio options
                "--embed-thumbnail", "--add-metadata"  # Metadata
            ]
        elif self.download_type == "thumbnail":
            command = base_command + cookie_option + [
            "--skip-download", "--write-thumbnail" # Thumbnail options
            ]
        else:
            command = base_command # Default

        print(f"[WORKER] Generated yt-dlp command: {command}")  # Debug: Command built
        return command  # Return command

    def execute_yt_dlp(self, command, temp_output_dir):
        """Executes yt-dlp and captures stdout and stderr for processing."""
        print(f"[WORKER] Executing yt-dlp command...")  # Debug: Command execution

        # First get video info to display title and artist (with cookie support)
        try:
            # Find URL in command
            url = None
            for arg in reversed(command):
                if not arg.startswith('-') and not arg.startswith('http'):
                    continue
                if arg.startswith('http'):
                    url = arg
                    break

            if url:
                # Set up options including cookies
                cookie_option = r'Main Files/Configs/YouTube Downloader/www.youtube.com_cookies.txt'
                ydl_info_opts = {
                    'quiet': True,       # Suppress output
                    'no_warnings': True,  # Suppress warnings
                }

                # Add cookies if file exists
                if os.path.exists(cookie_option):
                    ydl_info_opts['cookiefile'] = cookie_option
                    print(f"[WORKER] Using cookie file for video info: {cookie_option}")

                # Extract video metadata
                with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    title = info_dict.get('title', 'Unknown')
                    artist = info_dict.get('artist') or info_dict.get('uploader') or 'Unknown'

                    # Limit title length
                    max_title_length = 35
                    if len(title) > max_title_length:
                        title = title[:max_title_length-3] + "..."

                    # Limit artist length
                    max_artist_length = 25
                    if len(artist) > max_artist_length:
                        artist = artist[:max_artist_length-3] + "..."

                    # Format video info
                    self.video_info = f"{title} -> {artist} ->"
            else:
                self.video_info = "Unknown -> Unknown ->"
                print("[WORKER] Could not extract URL from command")
        except Exception as e:
            print(f"[ERROR] Couldn't get video info: {e}")
            self.video_info = "Unknown -> Unknown ->"

        # Start download process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.PIPE,  # Capture stderr
            text=True,  # Text mode
            creationflags=subprocess.CREATE_NO_WINDOW  # Hide console
        )

        print(f"[WORKER] yt-dlp process started (PID: {process.pid})") # Debug: Process launched

        # Process stdout for progress
        for line in process.stdout:
            if not self.isRunning:  # Check if canceled
                print("[WORKER] Download canceled, terminating yt-dlp")  # Debug: Cancel during execution
                process.terminate()  # Kill process
                return
            # Extract progress
            progress = self.extract_progress(line)
            if progress:
                self.progress_signal.emit(progress)  # Send progress
            # Check for speed info
            if "KiB/s" in line or "MiB/s" in line:
                cleaned_line = ' '.join(line.strip().split())  # Clean line
                self.speed_signal.emit(f"{self.video_info} {cleaned_line}")  # Send speed

        # Process stderr for errors
        for err_line in process.stderr:
            if err_line.strip():  # Non-empty lines
                self.error_signal.emit(f"Error: {err_line.strip()}")  # Send error

        process.wait()  # Wait for completion
        print(f"[WORKER] yt-dlp process completed (exit code: {process.returncode})")  # Debug: Process complete

        # Move downloaded files
        self.move_downloaded_files(temp_output_dir)

    def move_downloaded_files(self, temp_output_dir):
        """Moves downloaded files from the temporary directory to the user-selected output directory."""
        print(f"[WORKER] Moving files from {temp_output_dir} to {self.output_dir}")  # Debug: File moving
        for file in os.listdir(temp_output_dir):  # Process each file
            source_path = os.path.join(temp_output_dir, file)
            dest_path = os.path.join(self.output_dir, file)
            print(f"[WORKER] Processing file: {file}")

            if self.download_type == "video" and file.endswith(".mp4"):  # Video files
                unique_filename = self.get_unique_filename(self.output_dir, file)  # Get unique name
                dest_path = os.path.join(self.output_dir, unique_filename)
                print(f"[WORKER] Moving video file: {source_path} to {dest_path}")  # Debug: Video move
                shutil.move(source_path, dest_path)  # Move file
                self.file_moved_signal.emit(f"Moved: {file}")  # Signal moved

            elif self.download_type == "audio" and file.endswith((".opus")):  # Audio files
                unique_filename = self.get_unique_filename(self.output_dir, file)  # Get unique name
                dest_path = os.path.join(self.output_dir, unique_filename)
                print(f"[WORKER] Moving audio file: {source_path} to {dest_path}")  # Debug: Audio move
                shutil.move(source_path, dest_path)  # Move file
                self.file_moved_signal.emit(f"Moved: {file}")  # Signal moved

            elif self.download_type == "thumbnail" and file.endswith(".webp"):  # Thumbnails
                unique_filename = self.get_unique_filename(self.output_dir, file)  # Get unique name
                dest_path = os.path.join(self.output_dir, unique_filename)
                print(f"[WORKER] Moving thumbnail file: {source_path} to {dest_path}")  # Debug: Thumbnail move
                shutil.move(source_path, dest_path)  # Move file
                self.file_moved_signal.emit(f"Moved: {file}")  # Signal moved
            else:
                print(f"[WORKER] Skipping file: {file} (Type: {self.download_type})") #Debug: File skipped

    def get_unique_filename(self, directory, filename):
        """Ensures no file overwrites occur by appending a counter if needed."""
        base, ext = os.path.splitext(filename)  # Split filename
        counter = 1  # Initialize counter
        new_filename = filename  # Start with original
        print(f"[WORKER] Checking for unique filename for: {filename}")  # Debug: Uniqueness check
        while os.path.exists(os.path.join(directory, new_filename)):  # While exists
            new_filename = f"{base}({counter}){ext}"  # Add counter
            counter += 1  # Increment
            print(f"[WORKER] Filename exists, trying variant: {new_filename}")  # Debug: Variant attempt
        print(f"[WORKER] Final unique filename: {new_filename}")  # Debug: Unique name found
        return new_filename  # Return unique name

    def extract_progress(self, line):
        """Extracts and returns progress percentage from yt-dlp output."""
        progress_match = re.search(r"(\d+\.?\d*)%", line)  # Search for percentage
        if progress_match:  # If found
            progress = int(float(progress_match.group(1)))
            print(f"[DEBUG] Progress update: {progress}%")  # VERY verbose, comment out unless needed
            return progress  # Return progress
        return None  # Return None if no progress


if __name__ == "__main__":
    print("[APP] Starting YouTube Downloader application...")  # Debug: Application start
    app = QApplication(sys.argv)  # Create application
    print("[APP] Setting the whole UI font to Comic Sans MS...")  # Debug: Font Setup
    comic_sans_font = QFont("Comic Sans MS", 9)  # Create font
    app.setFont(comic_sans_font)  # Set application font
    print("[APP] Comic Sans MS Font has been set for the whole UI")  # Debug: Font Setup Completion
    window = YouTubeDownloaderApp()  # Create main window
    window.show()  # Show window
    print("[APP] Application running, main window displayed")  # Debug: Running state
    sys.exit(app.exec())  # Start event loop