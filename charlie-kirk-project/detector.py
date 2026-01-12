import cv2
import mediapipe as mp
import pygame
import json
from PIL import Image
from pathlib import Path
import time
import threading


class CharlieKirkDetector:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

        # Initialize components
        pygame.mixer.init()
        self.sound = None
        self.load_sound()

        self.face_mesh_landmarks = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.spam_folder = Path("assets/spam")

        # Detection state
        self.timer_started = None
        self.playing = False
        self.running = False
        self.cam = None
        self.detection_thread = None

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "timer": 2.0,
                "iris_threshold": 0.35,
                "spam_loops": 4,
                "sound_enabled": True,
                "sound_path": "./assets/we-are-charlie-kirk-song.mp3",
                "start_minimized": False
            }

    def reload_config(self):
        """Reload configuration (call after settings change)"""
        self.config = self.load_config()
        self.load_sound()

    def load_sound(self):
        """Load sound file"""
        try:
            if self.config["sound_enabled"] and Path(self.config["sound_path"]).exists():
                self.sound = pygame.mixer.Sound(self.config["sound_path"])
        except Exception as e:
            print(f"Error loading sound: {e}")
            self.sound = None

    def start_detection(self):
        """Start the detection in a separate thread"""
        if self.running:
            return

        self.running = True
        self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.detection_thread.start()

    def stop_detection(self):
        """Stop the detection"""
        self.running = False
        if self.cam:
            self.cam.release()
            cv2.destroyAllWindows()
        if self.detection_thread:
            self.detection_thread.join(timeout=2)

    def _detection_loop(self):
        """Main detection loop"""
        self.cam = cv2.VideoCapture(0)

        while self.running:
            ret, frame = self.cam.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            height, width, depth = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_image = self.face_mesh_landmarks.process(rgb_frame)
            face_landmark_points = processed_image.multi_face_landmarks

            if face_landmark_points:
                one_face_landmark_points = face_landmark_points[0].landmark

                # Left eye landmarks
                left = [one_face_landmark_points[145], one_face_landmark_points[159]]
                for landmark_point in left:
                    x = int(landmark_point.x * width)
                    y = int(landmark_point.y * height)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))

                # Right eye landmarks
                right = [one_face_landmark_points[374], one_face_landmark_points[386]]
                for landmark_point in right:
                    x = int(landmark_point.x * width)
                    y = int(landmark_point.y * height)
                    cv2.circle(frame, (x, y), 3, (255, 255, 0))

                # Iris positions
                l_iris = one_face_landmark_points[468]
                r_iris = one_face_landmark_points[473]

                # Calculate iris ratios
                l_ratio = (l_iris.y - left[1].y) / (left[0].y - left[1].y + 1e-6)
                r_ratio = (r_iris.y - right[1].y) / (right[0].y - right[1].y + 1e-6)

                current = time.time()
                threshold = self.config["iris_threshold"]

                # Check if looking down (doomscrolling)
                # When looking down, ratio DECREASES (iris moves up relative to eye landmarks)
                if (l_ratio < threshold) and (r_ratio < threshold):
                    if self.timer_started is None:
                        self.timer_started = current

                    # Timer exceeded - trigger spam
                    if (current - self.timer_started) >= self.config["timer"]:
                        if not self.playing:
                            self.trigger_spam()
                            self.playing = True
                else:
                    self.timer_started = None
                    self.playing = False

            cv2.imshow('Charlie-Kirkification - Face Detection', frame)
            key = cv2.waitKey(100)

            # ESC key to stop
            if key == 27:
                self.stop_detection()
                break

        if self.cam:
            self.cam.release()
            cv2.destroyAllWindows()

    def trigger_spam(self):
        """Trigger Charlie Kirk spam"""
        # Play sound
        if self.sound and self.config["sound_enabled"]:
            self.sound.play()

        # Spam images in a separate thread to not block detection
        spam_thread = threading.Thread(target=self._spam_images, daemon=True)
        spam_thread.start()

    def _spam_images(self):
        """Spam Charlie Kirk images"""
        try:
            for loop in range(self.config["spam_loops"]):
                for image_path in self.spam_folder.iterdir():
                    if image_path.suffix.lower() in ['.jpg', '.png', '.jpeg']:
                        im = Image.open(image_path)
                        im.show()
        except Exception as e:
            print(f"Error spamming images: {e}")


if __name__ == "__main__":
    # Test the detector
    detector = CharlieKirkDetector()
    detector.start_detection()

    try:
        # Keep running until interrupted
        while detector.running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        detector.stop_detection()
