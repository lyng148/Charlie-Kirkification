import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
from pathlib import Path
from detector import CharlieKirkDetector
from gui_settings import SettingsWindow


class CharlieKirkApp:
    def __init__(self):
        self.detector = CharlieKirkDetector()
        self.icon = None
        self.is_detecting = False

        # Load config to check start minimized
        if self.detector.config.get("start_minimized", False):
            self.start_detection()

    def create_icon_image(self):
        """Load icon from assets folder"""
        icon_path = Path("assets/icons/charlie-kirk-praying.png")
        return Image.open(icon_path)

    def start_detection(self, icon=None, item=None):
        """Start face detection"""
        if not self.is_detecting:
            self.is_detecting = True
            self.detector.reload_config()  # Reload config in case settings changed
            self.detector.start_detection()
            if self.icon:
                self.icon.notify("Charlie-Kirkification is now watching you!", "Detection Started")
            self.update_menu()

    def stop_detection(self, icon=None, item=None):
        """Stop face detection"""
        if self.is_detecting:
            self.is_detecting = False
            self.detector.stop_detection()
            if self.icon:
                self.icon.notify("Detection stopped. You can doomscroll freely now.", "Detection Stopped")
            self.update_menu()

    def toggle_detection(self, icon=None, item=None):
        """Toggle detection on/off"""
        if self.is_detecting:
            self.stop_detection()
        else:
            self.start_detection()

    def open_settings(self, icon=None, item=None):
        """Open settings window"""
        settings = SettingsWindow(self.detector.config_path)
        # Run in separate thread to avoid blocking
        settings_thread = threading.Thread(target=settings.show, daemon=True)
        settings_thread.start()

    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.stop_detection()
        if self.icon:
            self.icon.stop()

    def update_menu(self):
        """Update the tray menu"""
        if self.icon:
            self.icon.menu = self.create_menu()

    def create_menu(self):
        """Create system tray menu"""
        if self.is_detecting:
            toggle_text = "Stop Detection"
        else:
            toggle_text = "Start Detection"

        return pystray.Menu(
            item(toggle_text, self.toggle_detection),
            item("Settings", self.open_settings),
            pystray.Menu.SEPARATOR,
            item("Quit", self.quit_app)
        )

    def run(self):
        """Run the system tray application"""
        icon_image = self.create_icon_image()
        self.icon = pystray.Icon(
            "charlie_kirk",
            icon_image,
            "Charlie-Kirkification",
            menu=self.create_menu()
        )

        # Show notification on startup
        self.icon.notify(
            "Charlie-Kirkification is running in the system tray.\nRight-click the icon to access settings.",
            "App Started"
        )

        # Run the icon (this blocks until quit)
        self.icon.run()


if __name__ == "__main__":
    app = CharlieKirkApp()
    app.run()
