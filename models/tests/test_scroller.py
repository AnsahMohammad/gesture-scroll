import unittest
import cv2
import mediapipe as mp
from scroller import perform_scroll


class TestScrollFunction(unittest.TestCase):
    def setUp(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)

    def test_perform_scroll_neutral(self):
        frame = cv2.imread("./tests/test_image/neutral.png")
        current_state = "neutral"
        scroll_flag = False
        activation_flag = False
        PADDING = 50
        _, scroll_flag, activation_flag = perform_scroll(
            frame, self.hands, current_state, scroll_flag, activation_flag, PADDING
        )
        self.assertFalse(scroll_flag)
        self.assertFalse(activation_flag)

    # def test_perform_scroll_activation(self):
    #     frame = cv2.imread('./tests/test_image/activation.png')
    #     current_state = "neutral"
    #     scroll_flag = False
    #     activation_flag = False
    #     PADDING = 50
    #     _, scroll_flag, activation_flag = perform_scroll(frame, self.hands, current_state, scroll_flag, activation_flag, PADDING)
    #     self.assertFalse(scroll_flag)
    #     self.assertTrue(activation_flag)
    # doesn't work because cache needs minimum 5 images


if __name__ == "__main__":
    unittest.main()
