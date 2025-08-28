# 🀄~ YT-Downloader-by-Rane ~🀄
💪 A simple yet powerful YouTube downloader built around [yt-dlp](https://github.com/yt-dlp/yt-dlp)
 👆. This tool lets you download videos, audio, and thumbnails from YouTube with ease, while preserving proper metadata for all supported formats (.mp4, .opus, .webp).

😄 It also supports batch processing, so you can queue multiple links and let the tool handle everything automatically.

📽️ In addition, it comes bundled with a video compressor tool powered by [HandBrakeCLI](https://handbrake.fr/)
 ✨. This is especially useful if you want to reduce the size of downloaded videos without losing much quality.

🦾 Whether you want clean audio files, original thumbnails, or smaller compressed video files, this project provides a streamlined workflow with minimal setup.

<img width="1454" height="1510" alt="Screenshot 2025-08-28 150226" src="https://github.com/user-attachments/assets/193165d9-ab96-4fce-ac02-69a205871b79" />

🔧 Installation & Setup

**Follow these steps to set up the project on your system.**

1️⃣. Install Python

_This project requires Python 3.10 or above._

Download Python from the official site: python.org/downloads

During installation, make sure to check the box that says:

✅ “Add Python to PATH”

Verify installation by running:

```
python --version
```

You should see something like `Python 3.11.6`.


2️⃣. Clone the Repository
~~~
git clone https://github.com/RaneKun/YT-Downloader-by-Rane.git
cd YT-Downloader-by-Rane
~~~


3️⃣. Install Python Dependencies

_This project uses a `requirements.txt` file for all dependencies._ Run:
~~~
pip install -r requirements.txt
~~~

This will automatically install:

✅ PyQt6 → GUI framework

✅ ffmpeg-python → Python wrapper for FFmpeg

✅ yt-dlp → YouTube downloader backend

✅ requests → HTTP requests handling

✅ mutagen → Metadata/tag editing


4️⃣. Install FFmpeg

_This project requires FFmpeg (for video/audio processing)._

**Windows**

Download a build from ffmpeg.org/download
.

Extract the folder (e.g., `ffmpeg-2025-win64`) somewhere permanent (like `C:\ffmpeg`).

Add the `bin` folder to PATH:

Press `Win + R` → type `sysdm.cpl` → Advanced → Environment Variables.

Under System variables, select Path → Edit → New.

Add:
~~~
C:\ffmpeg\bin
~~~

Click OK on all windows.

Verify installation:
~~~
ffmpeg -version
~~~

**macOS (Homebrew)**
~~~
brew install ffmpeg
~~~

**Linux (Debian/Ubuntu)**
~~~
sudo apt update
sudo apt install ffmpeg
~~~

5️⃣. Install HandBrakeCLI (for optional video compression)

**Windows**

Download HandBrakeCLI from the official site: handbrake.fr/downloads

Extract the folder (e.g., `C:\HandBrake`).

Add the folder containing `HandBrakeCLI.exe` to PATH (same steps as FFmpeg).

**macOS (Homebrew)**
~~~
brew install handbrake
~~~

**Linux (Debian/Ubuntu)**
~~~
sudo apt update
sudo apt install handbrake-cli
~~~

Verify installation:
~~~
HandBrakeCLI --version
~~~

If `YouTube Downloader.pyw` and `Video Compressor.pyw` opens successfully, you’re good to go 🎉.
