import cv2
import mediapipe as mp
from gesture_model import fetch_gesture
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk

class HandDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Scroll")

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.status_label = tk.Label(root, text="Status: Not Running")
        self.status_label.pack()

        self.start_button = tk.Button(root, text="Start Detection", command=self.start_detection)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack()

        self.current_state = "neutral"
        self.scroll_flag = False
        self.PADDING = 50

        self.cap = None
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(max_num_hands=1)

    def start_detection(self):
        self.cap = cv2.VideoCapture(0)
        self.update_status("Status: Running")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.update_gui()

    def stop_detection(self):
        if self.cap:
            self.cap.release()
        self.update_status("Status: Not Running")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Reset state variables after stopping detection
        self.current_state = "neutral"
        self.scroll_flag = False

    def update_status(self, message):
        self.status_label.config(text=message)

    def update_gui(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    h, w, _ = frame.shape
                    x_min, y_min, x_max, y_max = w, h, 0, 0
                    for landmark in hand_landmarks.landmark:
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        if x < x_min:
                            x_min = x
                        if x > x_max:
                            x_max = x
                        if y < y_min:
                            y_min = y
                        if y > y_max:
                            y_max = y

                    x_min -= self.PADDING
                    x_max += self.PADDING
                    y_min -= self.PADDING
                    y_max += self.PADDING

                    hand_roi = frame[y_min:y_max, x_min:x_max]
                    if hand_roi.size == 0:
                        continue

                    gesture_label = fetch_gesture(hand_roi)

                    if self.current_state == "neutral":
                        if gesture_label == "up" or gesture_label == "down":
                            self.current_state = gesture_label
                            self.scroll_flag = True

                    elif self.current_state == "up" and gesture_label == "down":
                        self.current_state = "neutral"
                        self.scroll_flag = False

                    elif self.current_state == "down" and gesture_label == "up":
                        self.current_state = "neutral"
                        self.scroll_flag = False

                    if self.scroll_flag:
                        if self.current_state == "up":
                            pyautogui.scroll(-1)
                        elif self.current_state == "down":
                            pyautogui.scroll(1)

                    cv2.putText(frame, "Gesture: " + str(gesture_label), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.video_label.img = img
            self.video_label.config(image=img)
            self.root.after(10, self.update_gui)  # Call this function again after 10ms (for smooth video stream)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = HandDetectionApp(root)
    app.run()
