import cv2
import mediapipe as mp
from gesture_model import what_gesture

def draw_hand_rectangle(frame, hand_landmarks):
    h, w, _ = frame.shape

    # Get the bounding box coordinates for the hand region
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

    # Draw a rectangle around the hand region
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

def main():
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

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

                hand_roi = frame[y_min:y_max, x_min:x_max]
                if hand_roi.size == 0:
                    continue

                gesture_label = what_gesture(hand_roi)
                # Display the predicted gesture label on the frame
                cv2.putText(frame, "Gesture: " + str(gesture_label), (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Draw a rectangle around the hand region
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        cv2.imshow('Hand Detection', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
