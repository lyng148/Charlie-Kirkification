# Charlie-Kirkification - Development Guide

## Running the Application

### Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Features

1. **System Tray Icon**
   - Application runs in system tray (notification area)
   - Right-click the icon to access menu:
     - Start/Stop Detection
     - Settings
     - Quit

2. **Settings Window**
   - Timer Threshold: How long you can look down before triggering
   - Iris Detection Threshold: Sensitivity of eye tracking
   - Spam Loops: Number of times to repeat spam
   - Sound Enable/Disable
   - Sound File Selection
   - Start Minimized option

3. **Face Detection**
   - Uses webcam to track your face and eyes
   - Detects when you're looking down (doomscrolling)
   - Triggers Charlie Kirk spam after threshold time

## Building .exe

### Build Instructions
```bash
# Install PyInstaller (already in requirements.txt)
pip install pyinstaller

# Build using the spec file
pyinstaller charlie-kirk.spec

# The .exe will be in the dist/ folder
```

### Distribution
- The built .exe is standalone
- Make sure to include the `assets/` folder in the same directory as the .exe
- Users can simply run the .exe without installing Python

## File Structure
```
charlie-kirk-project/
├── main.py              # Entry point with system tray
├── detector.py          # Face/eye detection logic
├── gui_settings.py      # Settings window
├── config.json          # User settings (auto-created)
├── requirements.txt     # Dependencies
├── charlie-kirk.spec    # PyInstaller build config
└── assets/
    ├── spam/           # Charlie Kirk images
    └── we-are-charlie-kirk-song.mp3
```

## Configuration (config.json)
The app stores settings in `config.json`:
```json
{
    "timer": 2.0,                    // Seconds before triggering
    "iris_threshold": 0.7,           // Eye tracking sensitivity (0.5-0.9)
    "spam_loops": 4,                 // How many times to loop spam
    "sound_enabled": true,           // Enable/disable sound
    "sound_path": "./assets/...",    // Path to sound file
    "start_minimized": false         // Auto-start detection on launch
}
```

## Usage Tips

1. **First Run**: The app starts with detection OFF. Right-click tray icon and click "Start Detection"
2. **Settings**: Change settings anytime via tray menu. Stop and restart detection for changes to take effect
3. **Webcam Window**: When detection is active, a window shows your webcam feed with eye tracking points
4. **Close Webcam Window**: Press ESC in the webcam window to stop detection
5. **Exit App**: Right-click tray icon → Quit

## Troubleshooting

- **Camera not found**: Make sure no other app is using the webcam
- **Sound not playing**: Check sound file path in settings
- **Detection too sensitive**: Increase iris_threshold in settings
- **Detection not triggering**: Decrease iris_threshold in settings
