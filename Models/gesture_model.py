from tensorflow.keras.models import save_model, load_model
import cv2
import numpy as np

model = load_model("./gesture_detection_model.h5")

categories = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "11": 11,
    "12": 12,
    "13": 13,
    "14": 14,
    "15": 15,
    "16": 16,
    "17": 17,
    "18": 18,
    "19": 19,
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

# what_gesture(cv2.imread("1004.jpg"))
