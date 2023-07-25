# Gesture Scroll

### Working of Gesture-Scroll

The Gesture-based **Accessibility Tool** is an application that enables users to control their computer's scrolling functionality using hand gestures. The tool utilizes computer vision and deep learning techniques to detect hand gestures and interpret them as scrolling commands. Users can perform specific hand gestures in front of their webcam, and the tool will translate those gestures into scrolling actions on the computer screen.
Model Loading

## Main tasks
1. Detect Hand
2. Analyze the Hand Gesture
3. Perform action according to the gesture


## 1. Hand Detection

The tool employs the **Mediapipe library** for hand detection. It captures the video feed from the computer's webcam and processes each frame to detect any hands present. Once a hand is detected, the tool extracts the Region of Interest (ROI) around the hand using landmark points obtained from Mediapipe. The ROI is then used to predict the hand gesture.
Gesture Prediction

## 2. Analyze the Hand Gesture
Before predicting the hand gesture, the captured ROI is resized to a standard size of 50x50 pixels. The pixel values of the image are then normalized to a range between 0 and 1 to prepare it for input to the deep learning model.

The tool utilizes a **pre-trained deep learning model** for gesture detection. The model is loaded from a saved file, __"gesture_detection_model.h5"__ using TensorFlow's Keras API. This model has been trained to recognize four different hand gestures: "down," "neutral," "up," and "other," which correspond to scrolling commands.
Hand Detection

The deep learning model takes the preprocessed ROI as input and predicts the probability distribution over the four gestures ("down," "neutral," "up," and "other"). The gesture with the highest probability is selected as the predicted gesture label.
Gesture-based Scrolling

- Read more about the Model used <a href="./gesture-model.md">here</a>

## 3. Perform Action
The tool uses the predicted gesture label and the current state of scrolling to perform scrolling actions. Initially, the tool is in the "neutral" state, indicating that no scrolling is happening. When the user performs an "up" or "down" gesture, the tool transitions to the corresponding state and sets a "scroll_flag" to true.

During the "up" or "down" state, if the user performs the opposite gesture (e.g., "down" while in "up" state), the tool transitions back to the "neutral" state, and the "scroll_flag" is set to false.

While the "scroll_flag" is true, the tool uses the pyautogui library to perform scrolling actions on the computer. If the current state is "up," the tool scrolls down, and if the current state is "down," the tool scrolls up.
User Interface

The tool displays a window titled "Hand Detection" that shows the webcam feed with a rectangle drawn around the detected hand region. It also overlays the predicted gesture label on the video feed to provide real-time feedback to the user about the detected gesture.

## Future Improvements

* **Continuous model refinement:** We will continue to improve the gesture recognition model by gathering additional data and exploring advanced network architectures, ensuring higher accuracy and performance.
* **Multi-gesture vocabulary:** Expanding the gesture vocabulary will enable users to perform a broader range of actions, such as zooming, rotating, or switching between applications.
* **Personalization and adaptation:** We aim to incorporate user training capabilities, allowing individuals to customize gestures based on their preferences and comfort.

