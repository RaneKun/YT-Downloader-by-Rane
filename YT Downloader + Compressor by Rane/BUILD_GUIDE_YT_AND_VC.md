# 🏗️ Building YouTube Downloader & Video Compressor to EXE

Complete guide to convert your `.pyw` scripts to standalone `.exe` files with icons and background images.

---

## 🚀 Quick Start

### **YouTube Downloader**

1. **Prepare files:**
   ```
   Your Folder/
   ├── YouTube_Downloader.pyw
   ├── build_youtube_downloader.bat
   └── Main Files/
       ├── Assests/
       │   └── YouTube Downloader/
       │       ├── default_icon.ico
       │       └── default_background.jpg
       └── Configs/
           └── YouTube Downloader/
               └── output directory.txt
   ```

2. **Double-click** `build_youtube_downloader.bat`

3. **Wait** 3-5 minutes

4. **Find your .exe** in `dist\YouTube Downloader by Rane.exe`

---

### **Video Compressor**

1. **Prepare files:**
   ```
   Your Folder/
   ├── Video_Compressor.pyw
   ├── build_video_compressor.bat
   └── Main Files/
       ├── Assests/
       │   └── Video Compressor/
       │       ├── default_icon.ico
       │       └── default_background.jpg
       └── Configs/
           └── Video Compressor/
               ├── handbrake preset.json
               └── output directory.txt
   ```

2. **Double-click** `build_video_compressor.bat`

3. **Wait** 3-5 minutes

4. **Find your .exe** in `dist\Video Compressor by Rane.exe`

---

## 📂 File Structure Requirements

**IMPORTANT:** Keep the exact folder structure as shown above. PyInstaller needs to know where to find the files.

The build scripts expect:
- `Main Files/Assests/[App Name]/default_icon.ico`
- `Main Files/Assests/[App Name]/default_background.jpg`
- `Main Files/Configs/[App Name]/` (with config files)

---

## ⚙️ Build Process Explained

### **What the Build Scripts Do:**

1. ✅ Check if Python is installed
2. ✅ Install PyInstaller if needed
3. ✅ Verify all required files exist
4. ✅ Clean up old build files
5. ✅ Run PyInstaller with correct flags
6. ✅ Bundle icon, background, and configs
7. ✅ Create single `.exe` file
8. ✅ Clean up temporary files

### **PyInstaller Flags Used:**

```batch
pyinstaller ^
    --onefile                    # Single .exe (not folder)
    --windowed                   # No console window
    --name "App Name"            # Executable name
    --icon="path/to/icon.ico"   # Window icon
    --add-data "icon;folder/"    # Bundle icon file
    --add-data "bg;folder/"      # Bundle background
    --add-data "configs;folder/" # Bundle configs
    --clean                      # Clean cache
    --noconfirm                  # Overwrite without asking
    script.pyw
```

---

## 🔧 Changes Made to Scripts

### **Added resource_path() Function:**

```python
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        # PyInstaller creates temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Running in normal Python environment
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
```

### **Updated Icon Loading:**

**Before:**
```python
self.setWindowIcon(QIcon('Main Files/Assests/YouTube Downloader/default_icon.ico'))
```

**After:**
```python
self.setWindowIcon(QIcon(resource_path('Main Files/Assests/YouTube Downloader/default_icon.ico')))
```

### **Updated Background Loading:**

**Before:**
```python
self.set_background_image('Main Files/Assests/YouTube Downloader/default_background.jpg')
```

**After:**
```python
self.set_background_image(resource_path('Main Files/Assests/YouTube Downloader/default_background.jpg'))
```

---

## ✅ Testing Your EXE Files

### **After building:**

1. **Test in place:**
   - Go to `dist` folder
   - Run the `.exe`
   - Verify icon appears
   - Verify background loads
   - Test all functions

2. **Test when moved:**
   - Copy `.exe` to Desktop
   - Run from Desktop
   - Everything should work ✅

3. **Test on another PC:**
   - Copy `.exe` to USB
   - Test on different computer
   - Should work without Python! ✅

---

## 📊 Expected File Sizes

| Application | .exe Size |
|-------------|-----------|
| YouTube Downloader | ~20-30 MB |
| Video Compressor | ~18-25 MB |

**Why so large?**
- Includes Python interpreter (~15 MB)
- Includes PyQt6 libraries (~8 MB)
- Includes yt-dlp (Downloader only)
- Includes icon + background images
- Everything needed to run standalone!

---

## 🐛 Troubleshooting

### **Problem: "Python not recognized"**
**Solution:** Python not in PATH. Reinstall Python with "Add to PATH" checked.

### **Problem: "PyInstaller not found"**
**Solution:** Build script will auto-install it. Or run: `pip install pyinstaller`

### **Problem: "Icon file not found"**
**Solution:** 
- Make sure `Main Files` folder is in the same directory as build script
- Check folder structure matches exactly
- File names are case-sensitive

### **Problem: Build fails with "UnicodeDecodeError"**
**Solution:** Your Python files have Windows line endings. This is normal, build should still work.

### **Problem: .exe shows no icon**
**Solution:** 
- Make sure you're using the `.pyw` files
- Rebuild from scratch (delete `build` and `dist` folders first)
- Verify icon file is valid `.ico` format

### **Problem: .exe shows no background**
**Solution:**
- Check background image is `.jpg` format
- Verify path in code matches actual file location
- Try running from command line to see error messages

### **Problem: Antivirus blocks .exe**
**Solution:**
- This is a false positive (common with PyInstaller)
- Whitelist the .exe in your antivirus
- Or build on a computer with antivirus disabled
- Submit to antivirus vendor as false positive

---

## 🎯 Distribution

### **YouTube Downloader:**

**What users need:**
- ✅ Just the `.exe` file
- ✅ Nothing else! (all bundled)

**Optional dependencies:**
- Internet connection (to download videos)
- Cookie file (for age-restricted videos)

---

### **Video Compressor:**

**What users need:**
- ✅ The `.exe` file
- ⚠️ **HandBrakeCLI** (must be installed separately)
- ⚠️ **ffmpeg** (must be installed separately)

**Important:** The `.exe` bundles the preset file, but HandBrakeCLI and ffmpeg must be installed system-wide.

**Installation guide for users:**

1. **Install HandBrakeCLI:**
   - Download from: https://handbrake.fr/downloads.php
   - Choose "Command Line Version"
   - Add to system PATH

2. **Install ffmpeg:**
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH

3. **Verify installation:**
   ```cmd
   HandBrakeCLI --version
   ffmpeg -version
   ```

---

## 📝 Build Script Output Example

```
========================================
YouTube Downloader - Build to EXE
========================================

[INFO] Python detected successfully
[INFO] PyInstaller already installed
[INFO] Script file found: YouTube_Downloader.pyw
[INFO] Icon file found
[INFO] Background image found
[INFO] Cleaning up old build files...
[INFO] Cleanup complete

========================================
Starting PyInstaller build process...
========================================

This may take a few minutes...

... (PyInstaller output) ...

========================================
[SUCCESS] Build completed successfully!
========================================

The executable has been created in the 'dist' folder:
  dist\YouTube Downloader by Rane.exe

IMPORTANT: The executable includes all necessary files.
You can move it anywhere and it will work!

You can now:
  1. Run the .exe file to test it
  2. Move it to any location you want
  3. Create a desktop shortcut
  4. Share with others (they don't need Python!)
```

---

## 🔄 Rebuilding

If you need to rebuild (after making changes):

1. **Delete old build:**
   - Delete `build` folder
   - Delete `dist` folder

2. **Run build script again:**
   - Double-click the `.bat` file
   - Wait for completion

3. **Test the new .exe**

---

## 💡 Pro Tips

### **1. Create Shortcuts**
After building, create desktop shortcuts:
- Right-click `.exe` → Send to → Desktop (create shortcut)

### **2. Version Naming**
Consider renaming your .exe files with version numbers:
- `YouTube Downloader by Rane v2.0.exe`
- `Video Compressor by Rane v2.0.exe`

### **3. Distribute as ZIP**
When sharing, package as ZIP:
```
YouTube_Downloader_v2.0.zip
├── YouTube Downloader by Rane.exe
└── README.txt (usage instructions)
```

### **4. Keep Source Code**
Always keep your:
- Original `.pyw` files
- Fixed `.pyw` files
- `Main Files` folder
- Build scripts

**Never distribute just the .exe without keeping source!**

### **5. Test Before Sharing**
Before distributing to others:
- Test on a clean PC (without Python)
- Test all features work
- Test on Windows 10 and 11
- Verify file sizes are reasonable

---

## 🎨 Customization

### **Change Application Name:**

In build script, modify:
```batch
--name "Your Custom Name Here"
```

### **Change Icon:**

Replace the icon file in:
```
Main Files/Assests/[App]/default_icon.ico
```

Must be `.ico` format (not `.png` or `.jpg`)!

### **Change Background:**

Replace the background in:
```
Main Files/Assests/[App]/default_background.jpg
```

Can be `.jpg` or `.png` format.

### **Add More Files:**

To bundle additional files:
```batch
--add-data "path/to/file;destination/folder"
```

---

## 🔍 Understanding the Bundling

### **How PyInstaller Works:**

1. **Analysis Phase:**
   - Scans your script for imports
   - Finds all Python dependencies
   - Identifies required DLL files

2. **Collection Phase:**
   - Gathers all dependencies
   - Copies icon, background, configs
   - Packages everything together

3. **Bundling Phase:**
   - Creates single `.exe` file
   - Embeds Python interpreter
   - Compresses all files

4. **Runtime:**
   - User runs `.exe`
   - PyInstaller extracts to temp folder (`_MEIPASS`)
   - `resource_path()` finds files in temp folder
   - Application runs normally

---

## 📊 Comparison

| Aspect | Original .pyw | Built .exe |
|--------|--------------|------------|
| Requires Python | ✅ Yes | ❌ No |
| Requires PyQt6 | ✅ Yes | ❌ No |
| Requires yt-dlp | ✅ Yes | ❌ No (Downloader) |
| File size | ~50 KB | ~25 MB |
| Portable | ❌ No | ✅ Yes |
| Icon/Background | ✅ Works | ✅ Works (after fix) |
| Shareable | ❌ No | ✅ Yes |

---

## ✅ Final Checklist

Before considering build complete:

- [ ] Built both applications successfully
- [ ] Tested .exe in original location
- [ ] Tested .exe after moving to different folder
- [ ] Verified icon appears correctly
- [ ] Verified background loads correctly
- [ ] Tested all features work
- [ ] File size is reasonable (~20-30 MB)
- [ ] No error messages on startup
- [ ] (Compressor only) Verified HandBrakeCLI/ffmpeg availability

---

## 🎉 Success!

You now have:
- ✅ Fully portable `.exe` files
- ✅ Icons that work anywhere
- ✅ Backgrounds that work anywhere
- ✅ No Python installation required
- ✅ Ready to share with anyone!

---

## 📞 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Verify folder structure matches exactly
3. Try building on a different computer
4. Check PyInstaller documentation: https://pyinstaller.org/

---

**Happy Building! 🔨✨**

Your applications are now truly standalone and portable!
