import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Screen dimensions (using pyautogui)
screen_width, screen_height = pyautogui.size()

# Webcam dimensions
camera_width, camera_height = 640, 480

# Initialize MediaPipe Hand Tracking
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)

# Check camera
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Smoothening settings
smoothening = 5  # Higher value for smoother movement
dead_zone = 5  # Ignore small movements
max_step = 50  # Maximum pixels per frame

plocX, plocY = 0, 0

def map_coordinates(x, y, in_width, in_height, out_width, out_height):
    return int(np.interp(x, [0, in_width], [0, out_width])), int(np.interp(y, [0, in_height], [0, out_height]))

def is_clicking(hand_landmarks):
    index_x = hand_landmarks.landmark[8].x * camera_width
    index_y = hand_landmarks.landmark[8].y * camera_height
    middle_x = hand_landmarks.landmark[12].x * camera_width
    middle_y = hand_landmarks.landmark[12].y * camera_height
    distance = ((index_x - middle_x)**2 + (index_y - middle_y)**2)**0.5
    return distance < 30

def process_hands(image):
    global plocX, plocY

    image = cv2.GaussianBlur(image, (5, 5), 0)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
            )

            index_x = int(hand_landmarks.landmark[8].x * camera_width)
            index_y = int(hand_landmarks.landmark[8].y * camera_height)

            screen_x, screen_y = map_coordinates(
                index_x, index_y, camera_width, camera_height, screen_width, screen_height
            )

            if abs(screen_x - plocX) > dead_zone or abs(screen_y - plocY) > dead_zone:
                clocX = plocX * (1 - 1/smoothening) + screen_x * (1/smoothening)
                clocY = plocY * (1 - 1/smoothening) + screen_y * (1/smoothening)

                clocX = np.clip(clocX, plocX - max_step, plocX + max_step)
                clocY = np.clip(clocY, plocY - max_step, plocY + max_step)

                pyautogui.moveTo(clocX, clocY, duration=0.01)

                plocX, plocY = clocX, clocY

            if is_clicking(hand_landmarks):
                pyautogui.click()

    return image

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = process_hands(image)
    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
