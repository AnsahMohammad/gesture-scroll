import cv2
import os

# Directory to save captured images
directory = input("Enter directory name : ")
SAVE_DIR = f"data/{directory}"
os.makedirs(SAVE_DIR, exist_ok=True)

# Set up camera
cap = cv2.VideoCapture(0)

# Set the size of the rectangular window to capture the hand
WINDOW_WIDTH, WINDOW_HEIGHT = 200, 200

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Draw the rectangular window
    cv2.rectangle(frame, (frame.shape[1] // 2 - WINDOW_WIDTH // 2, frame.shape[0] // 2 - WINDOW_HEIGHT // 2),
                  (frame.shape[1] // 2 + WINDOW_WIDTH // 2, frame.shape[0] // 2 + WINDOW_HEIGHT // 2), (0, 255, 0), 2)

    cv2.imshow("Capture Hand Images", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # Press 'q' to exit the application
        break
    elif key == ord("c"):  # Press 'c' to capture the hand image
        # Crop the rectangular region containing the hand
        hand_roi = frame[
                   frame.shape[0] // 2 - WINDOW_HEIGHT // 2: frame.shape[0] // 2 + WINDOW_HEIGHT // 2,
                   frame.shape[1] // 2 - WINDOW_WIDTH // 2: frame.shape[1] // 2 + WINDOW_WIDTH // 2]

        # Save the captured hand image
        img_name = os.path.join(SAVE_DIR, f"hand_{len(os.listdir(SAVE_DIR))}.png")
        cv2.imwrite(img_name, hand_roi)
        print(f"Hand image saved as {img_name}")

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
