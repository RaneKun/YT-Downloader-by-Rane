# Import necessary classes from PyQt6 for creating the GUI
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QProgressBar, QFileDialog
    )
# QApplication: Manages application control flow and main settings
# QMainWindow: Provides a main application window
# QWidget: Base class for all UI objects
# QVBoxLayout: Lines up widgets vertically
# QHBoxLayout: Lines up widgets horizontally
# QPushButton: Creates clickable buttons
# QLabel: Displays text or images
# QProgressBar: Shows progress of an operation
# QFileDialog: Provides dialog for file selection

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
import time  # Provides time-related functions
import re  # Provides regular expression operations
import shutil  # Provides high-level file operations
import json  # Provides JSON parsing and serialization
import ffmpeg  # Provides video processing capabilities

# Worker thread class that handles video compression in the background
class CompressionWorker(QThread):
    # Define signals for communication with main thread
    progress_updated = pyqtSignal(int)  # Emits compression progress percentage
    status_updated = pyqtSignal(str)  # Emits status messages
    remaining_files_updated = pyqtSignal(int)  # Emits count of remaining files
    task_completed = pyqtSignal()  # Emits when compression is complete

    def __init__(self, input_files, output_dir, preset_file):
        # Initialize the worker thread with input parameters
        print("[WORKER] Initializing CompressionWorker...")  # Debug: Initialization
        super().__init__()  # Call parent class constructor
        self.input_files = input_files  # List of input video files
        self.output_dir = output_dir  # Directory to save compressed videos
        self.preset_file = preset_file  # Path to HandBrake preset file
        self.total_files = len(input_files)  # Total number of files to process
        self.processed_files = 0  # Counter for processed files
        # Regular expression to parse HandBrake progress output
        self.progress_regex = re.compile(
            r'Encoding: task \d+ of \d+, (\d+\.\d+) %'
            r' \((\d+\.\d+) fps, avg (\d+\.\d+) fps, ETA (\d{2}h\d{2}m\d{2}s)\)'
        )
        self.running = True  # Flag to control thread execution
        print(f"[WORKER] Worker initialized with {self.total_files} files, output dir: {output_dir}")  # Debug: Initialization complete

    def run(self):
        # Main method that runs when thread starts
        print("[WORKER] Starting compression process...")  # Debug: Process start
        try:
            # Load HandBrake preset file
            print("[WORKER] Loading HandBrake preset...")  # Debug: Preset loading
            with open(self.preset_file, 'r', encoding='utf-8') as f:
                preset_data = json.load(f)  # Read JSON preset file
                preset_name = preset_data['PresetList'][0]['PresetName']  # Extract preset name
                print(f"[WORKER] Loaded preset: {preset_name}")  # Debug: Preset loaded

            # Create temporary directory for processing
            print("[WORKER] Creating temp directory...")  # Debug: Directory creation
            temp_dir = 'C:\\Windows\\Temp\\YT video compressor by Rane 📼'  # Temp directory path
            os.makedirs(temp_dir, exist_ok=True)  # Create directory if it doesn't exist
            print(f"[WORKER] Temp directory ready: {temp_dir}")  # Debug: Directory ready

            # Process each input file
            for filename in self.input_files:
                if not self.running:  # Check if stop was requested
                    print("[WORKER] Compression stopped by user request")  # Debug: Stop
                    break  # Exit loop if stopped

                print(f"[WORKER] Processing file: {filename}")  # Debug: File processing
                self.progress_updated.emit(0)  # Reset progress for new file
                self.status_updated.emit(f"Processing: {os.path.basename(filename)}")  # Update status

                # Prepare file paths for current file
                base_name = os.path.splitext(os.path.basename(filename))[0]  # Get filename without extension
                compressed_video = os.path.join(temp_dir, f"{base_name}.mp4")  # Path for compressed video
                thumbnail_file = os.path.join(temp_dir, f"{base_name}.jpg")  # Path for thumbnail
                output_with_thumbnail = os.path.join(temp_dir, f"{base_name}_with_thumbnail.mp4")  # Final output path

                # Clean up temp directory for new file
                print("[WORKER] Cleaning up temp directory for new file...")  # Debug: Cleanup
                if os.path.exists(temp_dir):  # Check if directory exists
                    shutil.rmtree(temp_dir)  # Remove directory and contents
                os.makedirs(temp_dir, exist_ok=True)  # Recreate directory

                # Process the video through all steps
                print("[WORKER] Extracting thumbnail...")  # Debug: Thumbnail extraction
                self.extract_thumbnail(filename, thumbnail_file)  # Extract thumbnail
                print("[WORKER] Compressing video...")  # Debug: Compression start
                self.compress_video(filename, compressed_video, preset_name)  # Compress video
                print("[WORKER] Merging thumbnail...")  # Debug: Thumbnail merge
                self.merge_thumbnail(compressed_video, thumbnail_file, output_with_thumbnail)  # Merge thumbnail
                print("[WORKER] Cleaning up temp files...")  # Debug: Cleanup
                self.cleanup_temp_files(thumbnail_file, compressed_video)  # Remove temp files
                print("[WORKER] Renaming files...")  # Debug: Renaming
                self.rename_files(temp_dir)  # Rename output files
                print("[WORKER] Moving files to output directory...")  # Debug: File moving
                self.move_files(temp_dir, self.output_dir)  # Move to final destination

                # Update counters and progress
                self.processed_files += 1  # Increment processed count
                remaining = self.total_files - self.processed_files  # Calculate remaining
                self.remaining_files_updated.emit(remaining)  # Update remaining count
                print(f"[WORKER] File processed ({self.processed_files}/{self.total_files}), {remaining} remaining")  # Debug: Progress

            # All files processed successfully
            print("[WORKER] All files processed successfully")  # Debug: Completion
            self.status_updated.emit("Processing complete! ✅")  # Update status
            self.task_completed.emit()  # Signal completion

        except Exception as e:  # Handle any errors
            print(f"[ERROR] Exception in worker thread: {str(e)}")  # Debug: Error
            self.status_updated.emit(f"Error: {str(e)}")  # Show error to user
            self.task_completed.emit()  # Signal completion (with error)

    def stop(self):
        # Method to stop the worker thread
        print("[WORKER] Stop requested...")  # Debug: Stop request
        self.running = False  # Set flag to stop processing

    def extract_thumbnail(self, video_file, thumbnail_file):
        # Extract thumbnail from video file
        print(f"[WORKER] Extracting thumbnail from {video_file} to {thumbnail_file}")  # Debug: Start
        try:
            print(f"[FFMPEG] Running thumbnail extraction command")  # Debug: Command
            # Use ffmpeg to extract thumbnail
            ffmpeg.input(video_file).output(thumbnail_file, map='0:v', vf='thumbnail', vframes=1).run()
            self.status_updated.emit(f"Thumbnail extracted: {os.path.basename(thumbnail_file)} (encoding progress will update soon ⌛)")  # Update status while addressing delays
            print("[WORKER] Thumbnail extraction successful")  # Debug: Success
        except ffmpeg.Error as e:  # Handle ffmpeg errors
            print(f"[ERROR] Thumbnail extraction failed: {e}")  # Debug: Error
            raise Exception(f"Error extracting thumbnail: {e}")  # Re-raise with custom message

    def compress_video(self, input_video, output_video, preset_name):
        # Compress video using HandBrakeCLI
        print(f"[WORKER] Starting video compression: {input_video} -> {output_video}")  # Debug: Start
        # Prepare HandBrake command
        handbrake_cmd = [
            'HandBrakeCLI',  # HandBrake command line tool
            '-i', input_video,  # Input video file
            '-o', output_video,  # Output video file
            '--preset-import-file', self.preset_file,  # Preset file to use
            '-Z', preset_name,  # Preset name to apply
            '--verbose=1'  # Verbose output for progress tracking
        ]
        print(f"[WORKER] HandBrake command: {' '.join(handbrake_cmd)}")  # Debug: Command

        try:
            print("[WORKER] Setting up clean English environment for subprocess")  # Debug: Env setup
            env = os.environ.copy()  # Copy current environment
            env['LANG'] = 'C'  # Set language to C (English)
            env['LC_ALL'] = 'C'  # Set locale to C
            env['LANGUAGE'] = 'C'  # Set language to C

            print("[WORKER] Starting HandBrake subprocess...")  # Debug: Process start
            # Start HandBrake process
            process = subprocess.Popen(
                handbrake_cmd,
                stdout=subprocess.PIPE,  # Capture standard output
                stderr=subprocess.STDOUT,  # Redirect stderr to stdout
                bufsize=1,  # Line buffered
                universal_newlines=True,  # Text mode
                encoding='utf-8',  # UTF-8 encoding
                errors='replace',  # Replace invalid characters
                creationflags=subprocess.CREATE_NO_WINDOW,  # No console window
                env=env  # Use modified environment
            )

            last_progress = 0  # Track last reported progress
            last_update_time = 0  # Track last update time

            # Process output line by line
            while self.running:  # Continue while not stopped
                line = process.stdout.readline()  # Read one line
                if not line:  # If no more output
                    if process.poll() is not None:  # Check if process finished
                        break  # Exit loop if done
                    continue  # Otherwise continue waiting

                # Log the raw output line for debugging
                print(f"[HANDBRAKE] {line.strip()}")  # Debug: Output

                # Check if line contains progress information
                match = self.progress_regex.search(line)
                if match:  # If progress info found
                    try:
                        # Extract progress values
                        percent_complete = float(match.group(1))  # Percentage complete
                        current_fps = match.group(2)  # Current FPS
                        avg_fps = match.group(3)  # Average FPS
                        eta = match.group(4)  # Estimated time remaining

                        # Ensure progress doesn't exceed 100%
                        if percent_complete >= 99.9:
                            percent_complete = 100.0

                        current_time = time.time()  # Get current time
                        # Only update if significant change or time elapsed
                        if (current_time - last_update_time > 0.1 or
                            int(percent_complete) != last_progress):

                            # Verbose progress logging
                            print(f"[PROGRESS] {percent_complete:.1f}% complete, "
                                f"Current FPS: {current_fps}, "
                                f"Avg FPS: {avg_fps}, "
                                f"ETA: {eta}")  # Debug: Progress

                            self.progress_updated.emit(int(percent_complete))  # Update progress
                            self.status_updated.emit(  # Update status message
                                f"Encoding: {os.path.basename(input_video)} - "
                                f"{percent_complete:.1f}% ({current_fps} fps, "
                                f"avg {avg_fps} fps, ETA {eta})"
                            )
                            last_progress = int(percent_complete)  # Update last progress
                            last_update_time = current_time  # Update last update time
                            QApplication.processEvents()  # Process GUI events
                    except Exception as e:  # Handle parsing errors
                        print(f"[WARNING] Error parsing progress line: {e}")  # Debug: Error

            # Compression completed successfully
            if self.running:  # If not stopped by user
                print("[WORKER] Compression completed successfully")  # Debug: Success
                self.progress_updated.emit(100)  # Set progress to 100%
                self.status_updated.emit(f"Compressed video created: {os.path.basename(output_video)}")  # Update status

            # Check for HandBrake errors
            if process.returncode != 0 and self.running:  # If error occurred
                print(f"[ERROR] HandBrakeCLI failed with return code {process.returncode}")  # Debug: Error
                raise Exception(f"HandBrakeCLI failed with return code {process.returncode}")  # Raise error

        except Exception as e:  # Handle other errors
            print(f"[ERROR] Video compression failed: {e}")  # Debug: Error
            raise Exception(f"Error compressing video: {e}")  # Re-raise with custom message

    def merge_thumbnail(self, video_path, image_path, output_path):
        # Merge thumbnail with video
        print(f"[WORKER] Merging thumbnail {image_path} with video {video_path}")  # Debug: Start
        # Prepare ffmpeg command
        ffmpeg_cmd = [
            'ffmpeg', '-i', video_path, '-i', image_path,  # Input files
            '-map', '0', '-map', '1',  # Map both streams
            '-c', 'copy',  # Copy streams without re-encoding
            '-disposition:v:1', 'attached_pic',  # Set thumbnail disposition
            output_path  # Output file
        ]
        print(f"[WORKER] FFmpeg command: {' '.join(ffmpeg_cmd)}")  # Debug: Command
        try:
            print(f"[FFMPEG] Starting thumbnail merge process")  # Debug: Process start
            subprocess.run(ffmpeg_cmd, check=True)  # Run ffmpeg command
            self.status_updated.emit(f"Merged thumbnail with video: {os.path.basename(output_path)}")  # Update status
            print("[WORKER] Thumbnail merge successful")  # Debug: Success
        except subprocess.CalledProcessError as e:  # Handle errors
            print(f"[ERROR] Thumbnail merge failed: {e}")  # Debug: Error
            raise Exception(f"Error merging thumbnail: {e}")  # Re-raise with custom message

    def cleanup_temp_files(self, thumbnail_file, video_file):
        # Clean up temporary files
        print("[WORKER] Cleaning up temporary files...")  # Debug: Start
        for file in [thumbnail_file, video_file]:  # Loop through files to delete
            try:
                os.remove(file)  # Delete file
                self.status_updated.emit(f"Deleted temporary file: {os.path.basename(file)}")  # Update status
                print(f"[WORKER] Deleted temp file: {file}")  # Debug: Deletion
            except FileNotFoundError:  # Handle missing files
                print(f"[WARNING] Temp file not found during cleanup: {file}")  # Debug: Warning
                pass  # Continue with next file

    def rename_files(self, directory):
        # Rename files in directory
        print(f"[WORKER] Renaming files in directory: {directory}")  # Debug: Start
        for filename in os.listdir(directory):  # Loop through files
            if filename.endswith(".mp4") and "_with_thumbnail" in filename:  # Check if needs renaming
                new_filename = filename.replace("_with_thumbnail", "")  # Remove suffix
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))  # Rename file
                self.status_updated.emit(f"Renamed file: {filename} to {new_filename}")  # Update status
                print(f"[WORKER] Renamed: {filename} -> {new_filename}")  # Debug: Rename

    def get_unique_filename(self, directory, filename):
        # Generate unique filename to avoid overwrites
        print(f"[WORKER] Generating unique filename for {filename} in {directory}")  # Debug: Start
        base, ext = os.path.splitext(filename)  # Split filename and extension
        counter = 1  # Start counter at 1
        new_filename = filename  # Start with original filename
        while os.path.exists(os.path.join(directory, new_filename)):  # While filename exists
            new_filename = f"{base} ({counter}){ext}"  # Append counter
            counter += 1  # Increment counter
        print(f"[WORKER] Unique filename determined: {new_filename}")  # Debug: Result
        return new_filename  # Return unique filename

    def move_files(self, source_dir, destination_dir):
        # Move files from source to destination with unique names
        print(f"[WORKER] Moving files from {source_dir} to {destination_dir}")  # Debug: Start
        for filename in os.listdir(source_dir):  # Loop through source files
            source_file = os.path.join(source_dir, filename)  # Full source path
            if os.path.isfile(source_file):  # Check if it's a file (not directory)
                unique_filename = self.get_unique_filename(destination_dir, filename)  # Get unique name
                destination_file = os.path.join(destination_dir, unique_filename)  # Full destination path
                shutil.move(source_file, destination_file)  # Move file
                self.status_updated.emit(f'Moved to output: {unique_filename}')  # Update status
                print(f"[WORKER] Moved file: {source_file} -> {destination_file}")  # Debug: Move

# Main application window class
class VideoCompressorApp(QMainWindow):
    def __init__(self):
        super().__init__()  # Call parent class constructor
        self.input_files = []  # List to store input files
        self.worker = None  # Worker thread reference
        print("[INIT] Initializing VideoCompressorApp main window...")  # Debug: Initialization
        self.setWindowTitle("Video Compressor by Rane")  # Set window title
        self.setWindowIcon(QIcon('Main Files/Assests/Video Compressor/default_icon.ico'))  # Set window icon
        self.output_dir = self.load_last_output_dir()  # Load last used output directory
        self.preset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Main Files/Configs/Video Compressor/handbrake preset.json')  # Preset file path
        print(f"[CONFIG] Loaded output directory: {self.output_dir}")  # Debug: Output dir
        self.init_ui()  # Initialize UI components
        print("[INIT] VideoCompressorApp initialization complete")  # Debug: Init complete

    def init_ui(self):
        # Initialize all UI components
        print("[UI] Initializing user interface components...")  # Debug: UI start
        self.resize(1300, 250)  # Set initial window size
        self.setMinimumSize(1300, 250)  # Set minimum window size
        self.center_window()  # Center window on screen

        self.init_background()  # Initialize background
        self.init_layouts()  # Initialize layouts
        self.init_output_selection()  # Initialize output selection
        self.init_action_buttons()  # Initialize action buttons
        self.init_progress_status()  # Initialize progress indicators
        self.init_central_widget()  # Initialize central widget
        print("[UI] User interface initialization complete")  # Debug: UI complete

    def init_background(self):
        # Initialize background image
        print("[UI] Setting up background image...")  # Debug: Background start
        self.background_label = QLabel(self)  # Create label for background
        self.set_background_image('Main Files/Assests/Video Compressor/default_background.jpg')  # Set background image
        print("[UI] Background setup complete")  # Debug: Background complete

    def init_layouts(self):
        # Initialize layout structures
        print("[UI] Creating layout structures...")  # Debug: Layout start
        main_layout = QVBoxLayout()  # Main vertical layout
        button_layout = QHBoxLayout()  # Horizontal layout for buttons
        output_layout = QHBoxLayout()  # Horizontal layout for output selection
        self.main_layout = main_layout  # Store main layout reference
        self.button_layout = button_layout  # Store button layout reference
        self.output_layout = output_layout  # Store output layout reference
        print("[UI] Layout structures created")  # Debug: Layout complete

    def init_output_selection(self):
        # Initialize output directory selection components
        print("[UI] Configuring output directory selection...")  # Debug: Output start
        self.output_label = QLabel(f"Selected output folder: {self.output_dir}")  # Label to show output dir
        self.browse_button = QPushButton("Browse Output Folder 📁")  # Button to browse output
        self.browse_button.clicked.connect(self.select_output_folder)  # Connect click handler

        self.open_folder_button = QPushButton("Open Output Folder 📂")  # Button to open output
        self.open_folder_button.clicked.connect(self.open_output_folder)  # Connect click handler

        # Add widgets to output layout
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.browse_button)
        self.output_layout.addWidget(self.open_folder_button)
        self.main_layout.addLayout(self.output_layout)  # Add to main layout
        print("[UI] Output directory selection configured")  # Debug: Output complete

    def init_action_buttons(self):
        # Initialize action buttons
        print("[UI] Setting up action buttons...")  # Debug: Buttons start
        self.input_button = QPushButton("Browse Input Files 📼️")  # Button to select input files
        self.input_button.clicked.connect(self.select_input_files)  # Connect click handler
        self.button_layout.addWidget(self.input_button)  # Add to button layout

        self.start_button = QPushButton("Start ⚡")  # Button to start compression
        self.start_button.clicked.connect(self.start_compression)  # Connect click handler
        self.button_layout.addWidget(self.start_button)  # Add to button layout

        self.main_layout.addLayout(self.button_layout)  # Add button layout to main
        print("[UI] Action buttons configured")  # Debug: Buttons complete

    def init_progress_status(self):
        # Initialize progress indicators
        print("[UI] Setting up progress indicators...")  # Debug: Progress start
        self.progress_bar = QProgressBar()  # Create progress bar
        self.progress_bar.setMaximum(100)  # Set max value (100%)
        self.progress_bar.setValue(0)  # Set initial value (0%)
        self.main_layout.addWidget(self.progress_bar)  # Add to main layout

        self.input_files_label = QLabel("Selected files: 0")  # Label for file count
        self.main_layout.addWidget(self.input_files_label)  # Add to main layout
        self.remaining_files_label = QLabel("Remaining files: 0")  # Label for remaining files
        self.main_layout.addWidget(self.remaining_files_label)  # Add to main layout

        self.speed_label = QLabel("Status: Idle (buttons will remain non-clickable and ui will remain non-scalable till compression completes, please be patient) ✌️")  # Status label
        self.main_layout.addWidget(self.speed_label)  # Add to main layout
        print("[UI] Progress indicators ready")  # Debug: Progress complete

    def init_central_widget(self):
        # Initialize central widget container
        print("[UI] Creating central widget container...")  # Debug: Central start
        central_widget = QWidget()  # Create central widget
        central_widget.setLayout(self.main_layout)  # Set main layout
        self.setCentralWidget(central_widget)  # Set as central widget
        print("[UI] Central widget ready")  # Debug: Central complete

    def center_window(self):
        # Center the window on screen
        print("[WINDOW] Calculating window center position...")  # Debug: Center start
        screen_geometry = QApplication.primaryScreen().geometry()  # Get screen dimensions
        x = (screen_geometry.width() - self.width()) // 2  # Calculate x position
        y = (screen_geometry.height() - self.height()) // 2  # Calculate y position
        self.move(x, y)  # Move window to center
        print("[WINDOW] Window centered on screen")  # Debug: Center complete

    def set_background_image(self, image_path):
        # Set background image
        print(f"[UI] Loading background image from: {image_path}")  # Debug: Background load
        self.background_pixmap = QPixmap(image_path)  # Load image into pixmap
        self.update_background()  # Update background display
        print("[UI] Background image loaded and applied")  # Debug: Background complete

    def update_background(self):
        # Update background scaling
        print("[UI] Updating background scaling...")  # Debug: Background update
        if hasattr(self, 'background_pixmap'):  # Check if pixmap exists
            # Scale pixmap to window size while maintaining aspect ratio
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),  # Scale to window size
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,  # Keep aspect ratio
                Qt.TransformationMode.SmoothTransformation  # Smooth scaling
            )
            self.background_label.setPixmap(scaled_pixmap)  # Set scaled pixmap
            self.background_label.setGeometry(0, 0, self.width(), self.height())  # Set label size
            self.background_label.lower()  # Move to back
        print("[UI] Background scaling updated")  # Debug: Background update complete

    def resizeEvent(self, event):
        # Handle window resize events
        print("[WINDOW] Handling window resize event...")  # Debug: Resize start
        super().resizeEvent(event)  # Call parent class handler
        self.update_background()  # Update background to new size
        print("[WINDOW] Resize handled, background updated")  # Debug: Resize complete

    def set_window_resizable(self, resizable):
        """Enable or disable window resizing"""
        print(f"[WINDOW] Setting window resizable: {resizable}")  # Debug: Current operation

        if resizable:  # If enabling resizing
            print("[WINDOW] Enabling window resizing with minimum size 1300x250")  # Debug: Enabling resize
            self.setMinimumSize(1300, 250)  # Set minimum size
            self.setMaximumSize(16777215, 16777215)  # Qt default maximum size
            print("[WINDOW] Window resize limits set to default Qt maximum")  # Debug: Max size set
        else:  # If disabling resizing
            current_size = self.size()  # Get current size
            print(f"[WINDOW] Disabling window resizing, locking size to: {current_size.width()}x{current_size.height()}")  # Debug: Size being locked
            self.setFixedSize(current_size)  # Lock current size
            print("[WINDOW] Window size locked")  # Debug: Confirmation

    def select_input_files(self):
        # Open file dialog to select input files
        print("[FILES] Opening file selection dialog...")  # Debug: File dialog
        files, _ = QFileDialog.getOpenFileNames(  # Show file dialog
            self,  # Parent window
            "Select Video Files",  # Dialog title
            "",  # Start directory (empty for default)
            "MP4 Files (*.mp4)"  # File filter
        )

        if files:  # If files were selected
            print(f"[FILES] Selected files: {files}")  # Debug: Selected files
            print(f"[FILES] Number of selected items changed to: {len(files)}")  # Debug: Count
            self.input_files = files  # Store selected files
            self.input_files_label.setText(f"Selected files: {len(files)}")  # Update count display
            self.remaining_files_label.setText(f"Remaining files: {len(files)}")  # Update remaining
            self.update_button_states()  # Update button states
        else:  # If selection cancelled
            print("[FILES] File selection cancelled by user")  # Debug: Cancellation

    def open_output_folder(self):
        # Open output folder in file explorer
        print(f"[FOLDER] Attempting to open output folder: {self.output_dir}")  # Debug: Open
        if os.path.exists(self.output_dir):  # Check if folder exists
            os.startfile(self.output_dir)  # Open folder
            print("[FOLDER] Output folder opened successfully")  # Debug: Success
        else:  # If folder doesn't exist
            print(f"[ERROR] Output folder does not exist: {self.output_dir}")  # Debug: Error

    def select_output_folder(self):
        # Open dialog to select output folder
        print("[FOLDER] Opening folder selection dialog...")  # Debug: Dialog
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")  # Show dialog
        if folder:  # If folder selected
            self.output_dir = folder  # Store selected folder
            self.output_label.setText(f"Selected output folder: {self.output_dir}")  # Update display
            self.save_output_dir()  # Save to config
            print(f"[FOLDER] Selected output folder: {self.output_dir}")  # Debug: Selection
        else:  # If cancelled
            print("[FOLDER] Folder selection cancelled by user")  # Debug: Cancellation

    def load_last_output_dir(self):
        # Load last used output directory from config
        print("[CONFIG] Attempting to load last used output directory...")  # Debug: Load
        try:
            with open("Main Files/Configs/Video Compressor/output directory.txt", "r") as file:  # Open config file
                directory = file.read().strip()  # Read directory path
                if os.path.exists(directory):  # Check if directory exists
                    print(f"[CONFIG] Found valid output directory: {directory}")  # Debug: Success
                    return directory  # Return directory
        except FileNotFoundError:  # If config file doesn't exist
            print("[CONFIG] No output directory config found, using default")  # Debug: Default
            pass  # Continue to default
        default_dir = os.path.abspath("Output 📤")  # Default output directory
        print(f"[CONFIG] Using default output directory: {default_dir}")  # Debug: Default
        return default_dir  # Return default

    def save_output_dir(self):
        # Save current output directory to config
        print(f"[CONFIG] Saving current output directory: {self.output_dir}")  # Debug: Save
        os.makedirs("Main Files/Configs/Video Compressor", exist_ok=True)  # Create config dir if needed
        with open("Main Files/Configs/Video Compressor/output directory.txt", "w") as file:  # Open config file
            file.write(self.output_dir)  # Write directory
        print("[CONFIG] Output directory saved successfully")  # Debug: Success

    def update_button_states(self, compressing=False):
        # Update enabled state of buttons based on compression status
        print(f"[UI] Updating button states (compressing={compressing})...")  # Debug: Update
        self.start_button.setEnabled(not compressing and len(self.input_files) > 0)  # Enable start if not compressing and files selected
        self.browse_button.setEnabled(not compressing)  # Enable browse if not compressing
        self.input_button.setEnabled(not compressing)  # Enable input if not compressing
        self.set_window_resizable(not compressing)  # Control window resizability
        print("[UI] Button states updated")  # Debug: Update complete

    def start_compression(self):
        # Start video compression process
        print("[WORKER] start_compression() called")  # Method entry point

        if not self.input_files:  # Check if no files selected
            print("[WARNING] No input files selected - aborting compression")  # Debug: Warning
            self.speed_label.setText("Status: No files selected for compression! 🙄")  # Update status
            return  # Exit method

        print(f"[WORKER] Starting compression for {len(self.input_files)} files")  # Debug: File count
        print(f"[CONFIG] Output directory: {self.output_dir}")  # Debug: Output dir
        print(f"[CONFIG] Using preset file: {self.preset_file}")  # Debug: Preset

        self.update_button_states(compressing=True)  # Disable buttons
        self.progress_bar.setValue(0)  # Reset progress
        self.speed_label.setText("Status: Compression in progress... 😑")  # Update status
        print("[UI] UI updated with initial compression state")  # Debug: UI update

        # Create worker thread
        self.worker = CompressionWorker(
            input_files=self.input_files,  # Pass input files
            output_dir=self.output_dir,  # Pass output directory
            preset_file=self.preset_file  # Pass preset file
        )
        print("[WORKER] CompressionWorker created")  # Debug: Worker creation

        # Connect worker signals to UI updates
        self.worker.progress_updated.connect(self.progress_bar.setValue)  # Progress updates
        print("[WORKER] Connected progress_updated signal")  # Debug: Connection

        self.worker.status_updated.connect(self.speed_label.setText)  # Status updates
        print("[WORKER] Connected status_updated signal")  # Debug: Connection

        self.worker.remaining_files_updated.connect(  # Remaining files updates
            lambda count: self.remaining_files_label.setText(f"Remaining files: {count}")
        )
        print("[WORKER] Connected remaining_files_updated signal")  # Debug: Connection

        self.worker.task_completed.connect(self.compression_complete)  # Completion signal
        print("[WORKER] Connected task_completed signal")  # Debug: Connection

        self.worker.start()  # Start worker thread
        print("[WORKER] Worker thread started")  # Debug: Thread start

    def compression_complete(self):
        # Handle compression completion
        print("[WORKER] compression_complete() called")  # Method entry point
        self.update_button_states(compressing=False)  # Re-enable buttons
        self.worker = None  # Clear worker reference
        print("[WORKER] Compression completed - UI reset and worker cleared")  # Debug: Completion

    def closeEvent(self, event):
        """Ensure the worker thread is stopped before closing the application."""
        print("[APP] Application closing requested...")  # Debug: Close
        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():  # If worker running
            print("[WORKER] Stopping active worker thread...")  # Debug: Stop
            self.worker.stop()  # Stop worker
            self.worker.wait()  # Wait for thread to finish
            print("[WORKER] Worker thread stopped")  # Debug: Stopped
            self.set_window_resizable(True)  # Make sure window is resizable again
        event.accept()  # Accept close event
        print("[APP] Application closed")  # Debug: Closed

# Main application entry point
if __name__ == "__main__":
    print("[APP] Starting Video Compressor application...")  # Debug: App start
    app = QApplication(sys.argv)  # Create application instance
    print("[APP] Setting the whole UI font to Comic Sans MS...")  # Debug: Font
    comic_sans_font = QFont("Comic Sans MS", 9)  # Create Comic Sans font
    app.setFont(comic_sans_font)  # Set application font
    print("[APP] Comic Sans MS Font has been set for the whole UI")  # Debug: Font set
    window = VideoCompressorApp()  # Create main window
    window.show()  # Show window
    print("[APP] Application running, main window displayed")  # Debug: Running
    sys.exit(app.exec())  # Start event loop