# 📋 filepath_copier.py — What is it for?

`filepath_copier.py` is a PySide6-based developer utility designed to help you quickly collect **relative paths** to important project files and save them in a `.txt` file for later use.

It's ideal for:
- 🧹 Organizing file references for documentation or scripts
- 📦 Creating curated file lists to copy elsewhere
- 📁 Tracking key project files without needing version control

---

## 🛠️ Core Features

### 1. **Automatic Project Root Detection**
- The app identifies your project root by going **two levels up** from the script itself.
- It only allows file paths that live **within** that project root to ensure validity.

---

### 2. **Create or Use `.txt` Lists**
- On startup, you're prompted to either:
  - **Open an existing** `.txt` list  
  - **Create a new** `.txt` list  
- Files are saved in:  
  `dev_tools/file_path_copier/*.txt`

---

### 3. **Append File Paths Easily**
You can add files to the list using the **"Select..."** button:
- 📄 **Files…** — pick `.py`, `.md`, `.txt`, or `.json` files  
- 📁 **Folder…** — recursively finds and appends all allowed files in that folder

Each file is saved as a **relative path from the project root**, one per line.

---

### 4. **Live Session Viewer**
- The right panel shows a live list of what you've added in this session
- You can **clear** the session view (won’t affect the actual file)
- You can switch `.txt` lists at any time via the **"Output…"** button

---

### 5. **Start Over with Safety**
- "Start Over" clears the session and optionally **moves the active `.txt` list to the trash** (instead of deleting it directly)
- Read-only files are protected (won’t be deleted)

---

### 6. **Copy Listed Files to Another Folder**
- Use the **"Copy To…"** button to:
  - Select a destination folder
  - Automatically **copy all files listed in the current `.txt`** to that location
  - ✅ Folder structure is preserved  
  - ✅ Original files remain untouched  
  - ❌ Missing or unreadable files are skipped (with a message)

---

## ⚙️ Technical Notes

- Supported file types: `.py`, `.md`, `.txt`, `.json`
- List files are always stored in **UTF-8**
- Newlines are **normalized to LF (`\n`)** across platforms
- The tool uses `send2trash` for safe file deletion

---

## ✅ Example Use Cases

- 🗂️ Creating a curated list of files for export or zip bundling
- 📜 Generating source lists for mkdocs or other doc tools
- 📤 Copying all documentation files to a publishing folder
- 📑 Keeping track of all `.py` files involved in a release

---

## 📎 File Location Summary

- Tool location: `dev_tools/file_path_copier/filepath_copier.py`
- List outputs: `dev_tools/file_path_copier/*.txt`
- Session file format: plain text with relative paths

---

**Made for devs who want speed, structure, and simplicity.**
