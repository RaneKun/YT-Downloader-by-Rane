# 🀄~ YT-Downloader-by-Rane ~🀄
💪 A simple yet powerful YouTube downloader built around [yt-dlp](https://github.com/yt-dlp/yt-dlp).

👆 This tool lets you download videos, audio, and thumbnails from YouTube with ease, while preserving proper metadata for all supported formats (.mp4, .opus, .webp).

😄 It also supports batch processing, so you can queue multiple links and let the tool handle everything automatically.

📽️ In addition, it comes bundled with a video compressor tool powered by [HandBrakeCLI](https://handbrake.fr/downloads2.php).
This is especially useful if you want to reduce the size of downloaded videos without losing much quality! ✨

🦾 Whether you want clean audio files, original thumbnails, or smaller compressed video files, this project provides a streamlined workflow with minimal setup.

<img width="1454" height="1510" alt="Screenshot 2025-08-29 110855" src="https://github.com/user-attachments/assets/34cbfebf-a7d4-4da1-a158-30cf0586c558" />


🔧 Installation & Setup
=

**Follow these steps to set up the project on your system.**


1️⃣ **Install Python**

_This project requires [Python 3.10](https://www.python.org/) or above._

☝️ Make sure Python is added to PATH ☑️

(For that, during installation make sure to check the box that says:

✅ “Add Python to PATH”)

![download-python-for-windows-5](https://github.com/user-attachments/assets/b825b5c3-48dc-4a09-918e-c9b2b1087250)

Verify installation by running:

```
python --version
```

You should see something like `Python 3.11.6`.


2️⃣ **Clone the Repository**

**Make sure you have [Git](https://git-scm.com/downloads) installed**. Run these commands in your terminal 💻

Clone this repository
~~~
git clone https://github.com/RaneKun/YT-Downloader-by-Rane.git
~~~

3️⃣ **Install Python Dependencies**

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


4️⃣ **Install FFmpeg**

_This project requires [FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) (for video/audio processing)._

🪟 **Windows**

Download a build for your specific OS from https://github.com/BtbN/FFmpeg-Builds/releases.

Extract the folder (e.g., `ffmpeg-2025-win64`) somewhere permanent (like `C:\ffmpeg`).

Add the `bin` folder to PATH:

Press `Win + R` → type `sysdm.cpl` → Advanced → Environment Variables.

Under System variables, select Path → Edit → New.

<img width="1138" height="1225" alt="Screenshot 2025-08-29 115903" src="https://github.com/user-attachments/assets/5f44c5af-69b1-45af-8591-30171be828a9" />

Add:
~~~
C:\ffmpeg\bin
~~~

Click OK on all windows.

Verify installation:
~~~
ffmpeg -version
~~~

🍎 **macOS (Homebrew)**
~~~
brew install ffmpeg
~~~

🐧 **Linux (Debian/Ubuntu)**
~~~
sudo apt update
sudo apt install ffmpeg
~~~


5️⃣ Install [HandBrakeCLI](https://handbrake.fr/downloads2.php) (for optional video compression)

🪟 **Windows**

Download HandBrakeCLI from the official site: https://handbrake.fr/downloads2.php

Extract the folder (e.g., `C:\HandBrake`).

Add the folder containing `HandBrakeCLI.exe` to PATH (same steps as FFmpeg).

🍎 **macOS (Homebrew)**
~~~
brew install handbrake
~~~

🐧 **Linux (Debian/Ubuntu)**
~~~
sudo apt update
sudo apt install handbrake-cli
~~~

Verify installation:
~~~
HandBrakeCLI --version
~~~

If `YouTube Downloader.pyw` and `Video Compressor.pyw` opens successfully, you’re good to go 🎉.



How to use it? 🤔
=

First copy and paste all YouTube **video** links, not playlists, not channels, only video links into that text box, one link per line ✅

<img width="952" height="366" alt="Screenshot 2025-08-30 092537" src="https://github.com/user-attachments/assets/4cd1da22-8d0d-465d-ada4-e181425d5fce" />

Next off select download type, weather you wanna download video, audio or thumbnail or you can download all three at once, just clcik on the checkbox ✔️

Then select your output directory, default is `C:\Users\Public\Videos` (as shown in the screenshot below)

Then finally hit the start button and wait for it to finish 😁

<img width="1430" height="430" alt="Screenshot 2025-08-30 093116" src="https://github.com/user-attachments/assets/c634d084-452e-4858-9aed-3dc101a168b0" />

