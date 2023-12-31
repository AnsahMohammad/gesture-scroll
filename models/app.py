"""
GUI Module for the scroller.py
"""
import tkinter as tk
import cv2
import mediapipe as mp

# pylint: disable=E0401, E1101, R0902, W0621

from PIL import Image, ImageTk
from scroller import perform_scroll


class HandDetectionApp:
    """
    Hand Gesture App Class
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Scroll")

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.status_label = tk.Label(root, text="Status: False")
        self.status_label.pack()

        self.start_button = tk.Button(
            root, text="Start Detection", command=self.start_detection
        )
        self.start_button.pack()

        self.stop_button = tk.Button(
            root, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED
        )
        self.stop_button.pack()

        self.current_state = "neutral"
        self.scroll_flag = False
        self.activation_flag = False
        self.padding = 50
        self.time_limit = 5

        self.cap = None
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(max_num_hands=1)

    def start_detection(self):
        """
        start detect
        """
        self.cap = cv2.VideoCapture(0)
        self.update_status("Status: False")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.update_gui()

    def stop_detection(self):
        """
        stop detect
        """
        if self.cap:
            self.cap.release()
        self.update_status("Status: False")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Reset state variables after stopping detection
        self.current_state = "neutral"
        self.scroll_flag = False
        self.activation_flag = False

    def update_status(self, message):
        """
        update status function
        """
        self.status_label.config(text=message)

    def update_gui(self):
        """
        GUI Updater
        """
        ret, frame = self.cap.read()
        if ret:
            self.current_state, self.scroll_flag, self.activation_flag = perform_scroll(
                frame,
                self.hands,
                self.current_state,
                self.scroll_flag,
                self.padding,
                self.time_limit,
            )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)

            # Update the status message to include activation_flag
            status_message = f"Status: {self.activation_flag}"
            self.update_status(status_message)

            self.video_label.img = img
            self.video_label.config(image=img)
            self.root.after(10, self.update_gui)

    def run(self):
        """
        Run function
        """
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = HandDetectionApp(root)
    app.run()
