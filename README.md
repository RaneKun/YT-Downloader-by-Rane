# 🀄~ YT-Downloader-by-Rane ~🀄
💪 A simple yet powerful YouTube downloader built around [yt-dlp](https://github.com/yt-dlp/yt-dlp).

👆 This tool lets you download videos, audio, and thumbnails from YouTube with ease, while preserving proper metadata for all supported formats (.mp4, .opus, .webp).

😄 It also supports batch processing, so you can queue multiple links and let the tool handle everything automatically.

<a id="video-compressor"></a>
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

-> PyQt6 → GUI framework

-> ffmpeg-python → Python wrapper for FFmpeg

-> yt-dlp → YouTube downloader backend

-> requests → HTTP requests handling

-> mutagen → Metadata/tag editing


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

1️⃣ Copy and paste all YouTube **video** links, not playlists, not channels, only video links into that text box, one link per line ✅

<img width="969" height="307" alt="Screenshot 2025-08-30 093800" src="https://github.com/user-attachments/assets/2231a9bc-69d1-4647-b777-a1ad3f30928b" />

2️⃣ Select download type, weather you wanna download video, audio or thumbnail or you can download all three at once, just clcik on the checkbox ✔️

3️⃣ Select your output directory, default is `C:\Users\Public\Videos` (as shown in the screenshot below)

4️⃣ Finally hit the start button and wait for it to finish 😁

<img width="1425" height="433" alt="Screenshot 2025-08-30 093823" src="https://github.com/user-attachments/assets/b6eb0bd9-4175-44a6-b77f-435bd1a30dd3" />

5️⃣ All of the necessary information, like the download progress, remaining files, file size, file name, eta, etc will be displayed at the bottom of the downloader in the `Status` part ✔️

<img width="1413" height="149" alt="Screenshot 2025-08-31 131838" src="https://github.com/user-attachments/assets/194ae41b-94f9-46b0-988c-8a4b060aae3a" />


Additional Features ➕
=

🟣 **Preview Links** 🔗🖇️

-> You can click on the Preview Link button to preview links before downloading them, this is especially useful during bulk downloading to check the links out before hitting download. 😁👍

-> It will show all the useful necessary information like thumbnail, title and channel name. 📝🖼️

<img width="2470" height="1858" alt="Screenshot 2025-08-31 124451" src="https://github.com/user-attachments/assets/81d3eec4-c3ca-4809-a458-d79a9e69c2bf" />

_Note that after clicking this button, the UI will freeze temporarily until it is done processing everything in the background and then return back to normal_ 👍✔️

🟣 **Load Cookies** 🍪🥠

-> You can click on the load cookies button to load your cookie file which will then allow you to download private/restricted content from youtube ⭕🔞

-> To get your cookie file you will need to download this very [extention](https://chromewebstore.google.com/detail/cclelndahbckbenkjhflpdbgdldlbecc?utm_source=item-share-cb) (_note that other similar extentions also do work but the file name might need to be modified, the default file name that is accepted by this downloader is - `www.youtube.com_cookies.txt`_) 🔰

-> Now to use this extention, simply open [YouTube](https://www.youtube.com/) and then clcik on extentions -> `Get cookies.txt LOCALLY` and then hit `Export` which will then download the `www.youtube.com_cookies.txt` file. 🍪

<img width="750" height="1029" alt="Screenshot 2025-08-31 125505" src="https://github.com/user-attachments/assets/c3013230-d0c3-4501-8b8e-327fafce8a56" />

<img width="1071" height="1257" alt="Screenshot 2025-08-31 125526" src="https://github.com/user-attachments/assets/d34ee59a-417a-429c-a8b8-e9a6daedebf4" />

<img width="723" height="243" alt="Screenshot 2025-08-31 125547" src="https://github.com/user-attachments/assets/c407ad8e-7549-4e2b-a202-886448871595" />

-> You will need to load this cookie file into the downloader, but remember that this cookie file **will expire within 15-30 minutes** _so you will need to repeat the process every now and then_, and I have tried to make it permanent but this is a yt-dlp limitation and besides, **there's a risk of getting your account banned** if the cookie file never expires, so this is better anyways and don't worry, _this is 100% safe, I have tried it with my very own account_ ⭐👍

~_again, remember that there's no need of this step and this is completely optional if you're just downloading casual stuff from YouTube_~

🟣 Bonus Tip ✨🗒️
=

-> If you want to grab all the links of a playlist or a channel and then copy paste them onto my downloader, then get this [extention](https://chromewebstore.google.com/detail/youtube-url-extractor/jmilibpbdpajjnabchfpfmmmjgbimefo) (or something similar) which will allow you to grab all the links of any playlist/channel. Thank me later 😁👍


Now to talk about the Video Compressor 📽️
=

I know, not many people are gonna be needing it really but I made it regardless because of two reasons

1️⃣ I needed it for my personal use, just like the downloader ✅

2️⃣ There is no option in my downloader to select the quality of the video file 🫠

How does the video compressor work? 🤔
=

Well am glad you asked! So most of it works the same way as the downloader, you just need to browse the **input files** _(which are the downloaded files of off my downloader)_ and then hit `Start` to start the compression ✔️
-> To tweak the compression swettings you will need to go to this directory first `YT Downloader + Compressor by Rane\Main Files\Configs\Video Compressor` and find the file called `handbrake preset.json` and edit it ✅

_Easy way to do that is by installing [handbrake](https://handbrake.fr/), creating a custom preset there for your requirement, and then exporting that as a `.json` file_ ✅📁

So do I even need to use your Video Compressor or can I directly use Handbrake? 🤔
=

Well good question lad! You can ofc use Handbrake here directly which has a far better UI than mine, (but not a cultured one 😆) but this compressor uses [Handbrake CLI](https://handbrake.fr/downloads2.php) as mentioned [before](#video-compressor) **And another very important part** handbrake won't retain metadata which is the whole reason why I started this project in the first place 😤 But my compressor will retain all metadata _just like how the downloader does_ 😁

This is for the curious geeks 🤓
=

If you wanna see what's happening in the background, everything, line-by-line, then just rename the extentions `.pyw` to `.py` and then run them on the terminal and check out all the debugging lines in detail ✌️
