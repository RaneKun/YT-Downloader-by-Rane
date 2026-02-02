@echo off
REM ============================================================================
REM Video Compressor - Build to EXE Script
REM This script compiles the Python script to a standalone .exe file
REM ============================================================================

echo.
echo ========================================
echo Video Compressor - Build to EXE
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Python detected successfully
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller not found. Installing PyInstaller...
    echo.
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller!
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] PyInstaller installed successfully
    echo.
) else (
    echo [INFO] PyInstaller already installed
    echo.
)

REM Check if the Python script exists
if not exist "Video_Compressor.pyw" (
    echo [ERROR] Video_Compressor.pyw not found in current directory!
    echo Please make sure the script is in the same folder as this batch file.
    pause
    exit /b 1
)

echo [INFO] Script file found: Video_Compressor.pyw
echo.

REM Check if required files exist
if not exist "Main Files\Assests\Video Compressor\default_icon.ico" (
    echo [ERROR] Icon file not found!
    echo Expected: Main Files\Assests\Video Compressor\default_icon.ico
    pause
    exit /b 1
)

if not exist "Main Files\Assests\Video Compressor\default_background.jpg" (
    echo [ERROR] Background image not found!
    echo Expected: Main Files\Assests\Video Compressor\default_background.jpg
    pause
    exit /b 1
)

if not exist "Main Files\Configs\Video Compressor\handbrake preset.json" (
    echo [ERROR] HandBrake preset file not found!
    echo Expected: Main Files\Configs\Video Compressor\handbrake preset.json
    pause
    exit /b 1
)

echo [INFO] Icon file found
echo [INFO] Background image found
echo [INFO] HandBrake preset found
echo.

REM Clean up old build files
echo [INFO] Cleaning up old build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "Video_Compressor.spec" del /q "Video_Compressor.spec"
echo [INFO] Cleanup complete
echo.

REM Build the executable
echo ========================================
echo Starting PyInstaller build process...
echo ========================================
echo.
echo This may take a few minutes...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "Video Compressor by Rane" ^
    --icon="Main Files/Assests/Video Compressor/default_icon.ico" ^
    --add-data "Main Files/Assests/Video Compressor/default_icon.ico;Main Files/Assests/Video Compressor/" ^
    --add-data "Main Files/Assests/Video Compressor/default_background.jpg;Main Files/Assests/Video Compressor/" ^
    --add-data "Main Files/Configs/Video Compressor;Main Files/Configs/Video Compressor" ^
    --clean ^
    --noconfirm ^
    Video_Compressor.pyw

REM Check if build was successful
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Build failed!
    echo ========================================
    echo.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Build completed successfully!
echo ========================================
echo.
echo The executable has been created in the 'dist' folder:
echo   dist\Video Compressor by Rane.exe
echo.
echo IMPORTANT: The executable includes all necessary files.
echo You can move it anywhere and it will work!
echo.
echo NOTES:
echo   - HandBrakeCLI and ffmpeg must be installed separately
echo   - Make sure HandBrakeCLI and ffmpeg are in your system PATH
echo.
echo You can now:
echo   1. Run the .exe file to test it
echo   2. Move it to any location you want
echo   3. Create a desktop shortcut
echo   4. Share with others (they need HandBrakeCLI + ffmpeg!)
echo.

REM Clean up build artifacts (optional)
echo [INFO] Cleaning up build artifacts...
if exist "build" rmdir /s /q "build"
if exist "Video_Compressor.spec" del /q "Video_Compressor.spec"
echo [INFO] Cleanup complete
echo.

echo ========================================
echo Build process finished!
echo ========================================
echo.
pause
