"""
Module to Generate the Image data for training the Deep Learning model
"""

import os
import time
import cv2
import mediapipe as mp

# Directory to save captured images
SAVE_DIR = input("Enter directory name: ")
os.makedirs(SAVE_DIR, exist_ok=True)


# Set up Mediapipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
WINDOW_WIDTH, WINDOW_HEIGHT = 100, 100
key = None

time.sleep(1)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame from BGR to RGB for Mediapipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract the hand ROI
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

            # Adjust the size of the hand frame
            x_min = max(0, x_min - WINDOW_WIDTH // 2)
            x_max = min(w, x_max + WINDOW_WIDTH // 2)
            y_min = max(0, y_min - WINDOW_HEIGHT // 2)
            y_max = min(h, y_max + WINDOW_HEIGHT // 2)

            hand_roi = frame[y_min:y_max, x_min:x_max]
            # print(f"Dimension: {x_max - x_min}, {y_max - y_min}")

            # Draw a rectangle around the hand region
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    cv2.imshow("Capture Hand Images", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # Press 'q' to exit the application
        break
    if key == ord("c"):  # Press 'c' to capture the hand image
        if hand_roi.size > 0:
            # Save the captured hand image
            img_name = os.path.join(
                SAVE_DIR, f"hand_{time.time()}_{len(os.listdir(SAVE_DIR))}.png"
            )
            cv2.imwrite(img_name, hand_roi)
            print(f"Hand image saved as {img_name}")

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
