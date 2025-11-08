import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
import os
import absl.logging
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

absl.logging.set_verbosity(absl.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class VirtualMouse:
    def __init__(self):
        # System Configuration
        self.wCam, self.hCam = 640, 480
        self.smoothening = 8
        self.frameR = 100
        self.plocX, self.plocY = 0, 0
        self.pTime = 0
        self.points_buffer = []
        self.buffer_length = 4
        
        # Camera Setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Hand Detector
        self.detector = htm.handDetector(maxHands=1, detectionCon=0.8, trackCon=0.8)
        self.wScr, self.hScr = pyautogui.size()
        
        # Audio Control (with error handling)
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.volume_available = True
            print("Volume control: ENABLED")
        except Exception as e:
            self.volume = None
            self.volume_available = False
            print("Volume control: DISABLED (not available on this system)")
    
    def draw_interface(self, img, fps):
        """System status overlay"""
        cv2.rectangle(img, (0,0), (300, 70), (50,50,50), cv2.FILLED)
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.putText(img, 'AI Mouse v2.3', (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    
    def process_gestures(self, img, lmList):
        try:
            if len(lmList) < 21:
                cv2.putText(img, "NO HAND DETECTED", (100, self.hCam//2), 
                           cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                return
                
            fingers = self.detector.fingersUp()
            
            # Improved Privacy Mode (only when all fingers closed)
            if sum(fingers) == 0:
                img[:] = 0
                cv2.putText(img, "PRIVACY MODE", (100, self.hCam//2), 
                           cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                self.points_buffer.clear()  # Clear movement buffer
                return
            else:
                # Reset buffer when exiting privacy mode
                if len(self.points_buffer) == 0:
                    self.plocX, self.plocY = 0, 0

            x1, y1 = lmList[8][1], lmList[8][2]

            # Cursor Movement (Index Finger)
            if fingers[1] and not fingers[2]:
                x3 = np.interp(x1, (self.frameR+50, self.wCam-self.frameR-50), (0, self.wScr))
                y3 = np.interp(y1, (self.frameR+50, self.hCam-self.frameR-50), (0, self.hScr))
                
                # Smoothing with weighted average
                self.points_buffer.append((x3, y3))
                if len(self.points_buffer) > self.buffer_length:
                    self.points_buffer.pop(0)
                
                weights = np.linspace(0.2, 1, len(self.points_buffer))
                x3_avg = np.average([p[0] for p in self.points_buffer], weights=weights)
                y3_avg = np.average([p[1] for p in self.points_buffer], weights=weights)
                
                clocX = self.plocX + (x3_avg - self.plocX) / self.smoothening
                clocY = self.plocY + (y3_avg - self.plocY) / self.smoothening
                
                pyautogui.moveTo(clocX, clocY)
                self.plocX, self.plocY = clocX, clocY
                
                cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
                cv2.putText(img, "MOVING", (x1-40, y1-30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2)

            # Left Click
            if fingers[1] and fingers[2]:
                length, img, _ = self.detector.findDistance(8, 12, img)
                if length < 35:
                    pyautogui.click()
                    cv2.putText(img, "CLICK", (x1-40, y1-30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            # Volume Control (only if available)
            if fingers[0] and fingers[4] and self.volume_available:
                length, img, _ = self.detector.findDistance(4, 20, img)
                vol = np.interp(length, [25, 220], [0.0, 1.0])
                self.volume.SetMasterVolumeLevelScalar(vol, None)
                cv2.putText(img, f'VOL: {int(vol*100)}%', (self.wCam-150, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        except Exception as e:
            print(f"Gesture error: {str(e)}")

    def run(self):
        print("\n=== AI Virtual Mouse Started ===")
        print("Controls:")
        print("  - Index finger up: Move cursor")
        print("  - Index + Middle pinch: Click")
        print("  - Thumb + Pinky: Volume control")
        print("  - Closed fist: Privacy mode")
        print("  - Press ESC to exit")
        print("================================\n")
        
        while True:
            success, img = self.cap.read()
            if not success: 
                continue
            
            img = cv2.flip(img, 1)
            img = self.detector.findHands(img)
            lmList = self.detector.findPosition(img)

            if len(lmList) > 0:
                self.process_gestures(img, lmList)

            # FPS Display
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            self.draw_interface(img, fps)

            cv2.imshow("AI Virtual Mouse", img)
            if cv2.waitKey(1) == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("\n=== AI Virtual Mouse Stopped ===\n")

if __name__ == "__main__":
    vm = VirtualMouse()
    vm.run()