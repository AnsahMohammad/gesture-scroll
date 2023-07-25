"""
Accessibility tool Module
"""
import cv2
import mediapipe as mp
from gesture_model import fetch_gesture
import pyautogui

def perform_scroll(frame, hands, current_state, scroll_flag, PADDING):
    """
    Perform scrolling based on hand gestures.

    Parameters:
        frame: The input video frame.
        hands: The mediapipe hands object.
        current_state: The current scrolling state.
        scroll_flag: Flag indicating if scrolling is enabled.
        PADDING: The increase in size for the hand region.

    Returns:
        current_state: The updated scrolling state.
        scroll_flag: The updated scrolling flag.
    """
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

            # Increase the size of the hand region
            x_min -= PADDING
            x_max += PADDING
            y_min -= PADDING
            y_max += PADDING

            hand_roi = frame[y_min:y_max, x_min:x_max]
            if hand_roi.size == 0:
                continue

            # Get the predicted gesture label
            gesture_label = fetch_gesture(hand_roi)

            # Perform scrolling based on the current state and the predicted gesture
            if current_state == "neutral":
                if gesture_label == "up" or gesture_label == "down":
                    current_state = gesture_label
                    scroll_flag = True

            elif current_state == "up" and gesture_label == "down":
                current_state = "neutral"
                scroll_flag = False

            elif current_state == "down" and gesture_label == "up":
                current_state = "neutral"
                scroll_flag = False

            # Perform the scrolling action
            if scroll_flag:
                if current_state == "up":
                    pyautogui.scroll(-1)  # Scroll down

                elif current_state == "down":
                    pyautogui.scroll(1)  # Scroll up

            # Display the predicted gesture label on the frame
            cv2.putText(
                frame,
                "Gesture: " + str(gesture_label),
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

            # Draw a rectangle around the hand region
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    return current_state, scroll_flag

# Main function to perform hand detection and scrolling
def main():
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)

    current_state = "neutral"
    scroll_flag = False

    PADDING = 50

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Call perform_scroll function to handle hand detection and scrolling
        current_state, scroll_flag = perform_scroll(frame, hands, current_state, scroll_flag, PADDING)

        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Check if the script is run directly
if __name__ == "__main__":
    main()
