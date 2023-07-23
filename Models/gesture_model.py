from tensorflow.keras.models import save_model, load_model
import cv2
import numpy as np

model = load_model("./gesture_detection_model.h5")

categories = {
    "down": 0,
    "neutral": 1,
    "up": 2,
    "other": 3
}

def what_gesture(new_img):
    # image_path = "1004.jpg"
    new_img = cv2.resize(new_img, (50, 50))
    new_img = new_img.astype("float32") / 255.0
    new_img = np.expand_dims(new_img, axis=0)  # Add a batch dimension

    predicted_probabilities = model.predict(new_img)
    predicted_label = np.argmax(predicted_probabilities)

    gesture_label = None
    for label, value in categories.items():
        if value == predicted_label:
            gesture_label = label
            break

    print("Predicted gesture label for the new image:", gesture_label)
    return gesture_label

what_gesture(cv2.imread("test/hand_5.png"))
