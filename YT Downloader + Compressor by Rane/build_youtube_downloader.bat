@echo off
REM ============================================================================
REM YouTube Downloader - Build to EXE Script
REM This script compiles the Python script to a standalone .exe file
REM ============================================================================

echo.
echo ========================================
echo YouTube Downloader - Build to EXE
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
if not exist "YouTube_Downloader.pyw" (
    echo [ERROR] YouTube_Downloader.pyw not found in current directory!
    echo Please make sure the script is in the same folder as this batch file.
    pause
    exit /b 1
)

echo [INFO] Script file found: YouTube_Downloader.pyw
echo.

REM Check if required files exist
if not exist "Main Files\Assests\YouTube Downloader\default_icon.ico" (
    echo [ERROR] Icon file not found!
    echo Expected: Main Files\Assests\YouTube Downloader\default_icon.ico
    pause
    exit /b 1
)

if not exist "Main Files\Assests\YouTube Downloader\default_background.jpg" (
    echo [ERROR] Background image not found!
    echo Expected: Main Files\Assests\YouTube Downloader\default_background.jpg
    pause
    exit /b 1
)

echo [INFO] Icon file found
echo [INFO] Background image found
echo.

REM Clean up old build files
echo [INFO] Cleaning up old build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "YouTube_Downloader.spec" del /q "YouTube_Downloader.spec"
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
    --name "YouTube Downloader by Rane" ^
    --icon="Main Files/Assests/YouTube Downloader/default_icon.ico" ^
    --add-data "Main Files/Assests/YouTube Downloader/default_icon.ico;Main Files/Assests/YouTube Downloader/" ^
    --add-data "Main Files/Assests/YouTube Downloader/default_background.jpg;Main Files/Assests/YouTube Downloader/" ^
    --add-data "Main Files/Configs/YouTube Downloader;Main Files/Configs/YouTube Downloader" ^
    --clean ^
    --noconfirm ^
    YouTube_Downloader.pyw

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
echo   dist\YouTube Downloader by Rane.exe
echo.
echo IMPORTANT: The executable includes all necessary files.
echo You can move it anywhere and it will work!
echo.
echo You can now:
echo   1. Run the .exe file to test it
echo   2. Move it to any location you want
echo   3. Create a desktop shortcut
echo   4. Share with others (they don't need Python!)
echo.

REM Clean up build artifacts (optional)
echo [INFO] Cleaning up build artifacts...
if exist "build" rmdir /s /q "build"
if exist "YouTube_Downloader.spec" del /q "YouTube_Downloader.spec"
echo [INFO] Cleanup complete
echo.

echo ========================================
echo Build process finished!
echo ========================================
echo.
pause
