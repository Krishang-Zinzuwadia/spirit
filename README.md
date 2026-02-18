# Spirit Voice Assistant

A sleek, Windows-native voice assistant  (Siri-like).

## Features
- **Siri-like Sphere UI**: Fullscreen, blurred, animated overlay.
- **Windows Automation**: Launch apps, lock PC, set timers (using native Clock app).
- **Background Mode**: Runs silently in tray; wake with **Ctrl+Space** or "Spirit".
- **Installer**: Installs to Program Files & auto-starts on login.

## Installation

### Option 1: Installer (Recommended)
Download `SpiritSetup.exe` from the Releases page and run it.

### Option 2: Run from Source
1. Clone repo:
   ```bash
   git clone https://github.com/Krishang-Zinzuwadia/spirit.git
   cd spirit
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Sarvam AI key in `.env`:
   ```bash
   SARVAM_API_KEY=your_key_here
   ```
4. Run (Must run as Admin first time to register hotkey):
   ```bash
   python main.py
   ```

## Building the Installer
1. Install PyInstaller: `pip install pyinstaller`
2. Install [Inno Setup 6](https://jrsoftware.org/isdl.php).
3. Run `build.bat` (as Administrator).
   - Result: `dist/SpiritSetup.exe`

## Skills
- **Wake Word**: "Spirit" (when not overlays)
- **Hotkey**: `Ctrl+Space` (show overlay + listen)
- **Commands**:
  - "Open [App Name]" (e.g., "Open VS Code", "Open Discord")
  - "Lock the PC" / "Lock screen"
  - "Set a timer for [X] minutes" (Automates Windows Clock)
  - "What time is it?"
  - "Sleep" (Puts PC to sleep)
