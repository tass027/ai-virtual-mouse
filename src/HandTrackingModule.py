
# import cv2
# import mediapipe as mp
# import numpy as np

# class handDetector:
#     def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.maxHands = maxHands
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#         self.lmList = []

#         self.mpHands = mp.solutions.hands.Hands(
#             static_image_mode=self.mode,
#             max_num_hands=self.maxHands,
#             min_detection_confidence=self.detectionCon,
#             min_tracking_confidence=self.trackCon
#         )
#         self.tipIds = [4, 8, 12, 16, 20]

#     def findHands(self, img):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = self.mpHands.process(imgRGB)
#         if results.multi_hand_landmarks:
#             for handLms in results.multi_hand_landmarks:
#                 mp.solutions.drawing_utils.draw_landmarks(
#                     img, handLms, mp.solutions.hands.HAND_CONNECTIONS)
#         return img

#     def findPosition(self, img):
#         self.lmList = []
#         results = self.mpHands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#         if results.multi_hand_landmarks:
#             try:
#                 hand = results.multi_hand_landmarks[0]
#                 for id in range(21):
#                     lm = hand.landmark[id]
#                     h, w = img.shape[:2]
#                     self.lmList.append([id, int(lm.x * w), int(lm.y * h)])
#             except:
#                 pass
#         return self.lmList

#     def fingersUp(self):
#         fingers = [0, 0, 0, 0, 0]
#         if len(self.lmList) < 21:
#             return fingers
            
#         # Thumb (X-axis comparison with wrist)
#         if self.lmList[4][0] > self.lmList[0][0]:
#             fingers[0] = 1

#         # Other fingers (Y-axis comparison)
#         for tip, idx in zip([8, 12, 16, 20], [1, 2, 3, 4]):
#             if self.lmList[tip][1] < self.lmList[tip-2][1] - 15:
#                 fingers[idx] = 1
#         return fingers

#     def findDistance(self, p1, p2, img):
#         if len(self.lmList) < max(p1, p2)+1:
#             return 0, img, None
            
#         x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
#         x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
#         length = int(np.hypot(x2-x1, y2-y1))
        
#         cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
#         return length, img, [x1, y1, x2, y2]
import cv2
import mediapipe as mp
import numpy as np

class handDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.8, trackCon=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.lmList = []

        self.mpHands = mp.solutions.hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.mpHands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    img, handLms, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img):
        self.lmList = []
        results = self.mpHands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            try:
                hand = results.multi_hand_landmarks[0]
                for id in range(21):
                    lm = hand.landmark[id]
                    h, w = img.shape[:2]
                    self.lmList.append([id, int(lm.x * w), int(lm.y * h)])
            except:
                pass
        return self.lmList

    def fingersUp(self):
        fingers = [0, 0, 0, 0, 0]
        if len(self.lmList) < 21:
            return fingers
            
        # Improved thumb detection
        if self.lmList[4][1] > self.lmList[2][1] + 10:  # More reliable reference point
            fingers[0] = 1

        # Relaxed finger detection
        for tip, idx in zip([8, 12, 16, 20], [1, 2, 3, 4]):
            if self.lmList[tip][2] < self.lmList[tip-2][2] - 8:  # Reduced threshold
                fingers[idx] = 1
        return fingers

    def findDistance(self, p1, p2, img):
        if len(self.lmList) < max(p1, p2)+1:
            return 0, img, None
            
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        length = int(np.hypot(x2-x1, y2-y1))
        
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
        return length, img, [x1, y1, x2, y2]