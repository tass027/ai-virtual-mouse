# 🖱️ AI Virtual Mouse - Hand Gesture Control System

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/opencv-4.5+-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/mediapipe-0.10+-orange.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Control your computer using hand gestures powered by AI! This innovative project eliminates the need for a physical mouse, offering an ergonomic and hygienic alternative for human-computer interaction.

## ✨ Features

- **✋ Touchless Mouse Control**: Control cursor with your index finger
- **🖱️ Gesture-Based Clicking**: Pinch fingers together to click
- **🔊 Volume Control**: Adjust system volume with hand distance
- **🔒 Privacy Mode**: Close your fist to instantly black out the screen
- **🎮 Interactive Game**: Gesture-controlled gaming experience (Gesture Defender)
- **⚡ Real-Time Processing**: Smooth 30 FPS hand tracking

## 🎮 Gesture Controls

| Gesture | Action | Visual Feedback |
|---------|--------|-----------------|
| ☝️ Index finger up | Move cursor | Purple circle on fingertip |
| 🤏 Index + Middle pinch (< 35px) | Left click | Green "CLICK" text |
| 🤙 Thumb + Pinky distance | Volume control (0-100%) | Volume percentage display |
| ✊ All fingers closed | Privacy mode | Screen blackout |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam
- Windows OS (for volume control features)

### Installation
```bash
# Clone the repository
git clone https://github.com/tass027/ai-virtual-mouse.git
cd ai-virtual-mouse

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Launch Virtual Mouse:**
```bash
python src/virtual_mouse.py
```

**Launch Volume Control:**
```bash
python src/volume_control.py
```

**Launch Gesture Defender Game:**
```bash
python src/games/gesture_defender.py
```

**Exit any application:** Press `ESC` key

## 🛠️ Technologies Used

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Python 3.8+** | Core programming language | [python.org](https://python.org) |
| **OpenCV** | Video capture & image processing | [opencv.org](https://opencv.org) |
| **MediaPipe** | Hand landmark detection (21 keypoints) | [mediapipe.dev](https://mediapipe.dev) |
| **NumPy** | Mathematical operations & data manipulation | [numpy.org](https://numpy.org) |
| **PyAutoGUI** | Mouse cursor control & click simulation | [pyautogui.readthedocs.io](https://pyautogui.readthedocs.io) |
| **Pycaw** | Windows audio control | [GitHub](https://github.com/AndreMiras/pycaw) |
| **Pygame** | Game development framework | [pygame.org](https://pygame.org) |

## 🏗️ Project Structure
```
ai-virtual-mouse/
├── src/
│   ├── virtual_mouse.py          # Main virtual mouse application
│   ├── HandTrackingModule.py     # Hand detection & tracking module
│   ├── volume_control.py         # Standalone volume control
│   └── games/
│       └── gesture_defender.py   # Gesture-controlled game
├── examples/
│   └── simple_hand_control.py    # Basic hand control example
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT License
└── README.md                      # This file
```

## 🎯 How It Works

### Architecture Flow
```
Webcam Feed
    ↓
OpenCV (Image Capture)
    ↓
MediaPipe (Hand Detection - 21 Landmarks)
    ↓
Gesture Recognition (Finger Position Analysis)
    ↓
Action Mapping (Movement/Click/Volume/Privacy)
    ↓
System Control (PyAutoGUI/Pycaw)
```

### Key Technical Features

- **Smoothing Algorithm**: Weighted averaging with 4-frame buffer for stable cursor movement
- **High Detection Accuracy**: 80% confidence threshold for reliable hand tracking
- **Optimized Performance**: 30+ FPS real-time processing
- **Low Latency**: < 50ms response time from gesture to action

## ⚙️ Configuration

Customize the behavior by editing these parameters in `src/virtual_mouse.py`:
```python
self.wCam, self.hCam = 640, 480    # Camera resolution
self.smoothening = 8                # Cursor smoothness (higher = smoother)
self.frameR = 100                   # Screen edge margin
self.buffer_length = 4              # Movement buffer size
detectionCon=0.8                    # Detection confidence (0.0-1.0)
trackCon=0.8                        # Tracking confidence (0.0-1.0)
```

## 🎮 Gesture Defender Game

A competitive dual-control game showcasing gesture recognition:

- **Gesture Player (Left)**: Control with hand gestures
- **Mouse Player (Right)**: Control with traditional mouse
- **Objective**: Shoot falling threats before they reach the bottom
- **Controls**:
  - Shoot: Pinch index + middle fingers (gesture) or left-click (mouse)
  - Deploy Shield: Pinch index + ring fingers (gesture) or right-click (mouse)
  - Speed Control: Adjust thumb-pinky distance (gesture only)

## 📊 Performance Metrics

- **FPS**: 30+ frames per second
- **Latency**: < 50ms gesture-to-action
- **Accuracy**: 95%+ gesture recognition rate
- **Tracking Range**: 30-80cm from camera (optimal)

## 🔧 Troubleshooting

### Camera Not Found
```python
# Test available cameras
import cv2
for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} works!")
        cap.release()
```

### Low FPS / Performance Issues
- Close unnecessary background applications
- Reduce camera resolution in code
- Ensure good lighting conditions
- Lower detection confidence values

### Gestures Not Recognized
- Maintain 30-50cm distance from camera
- Ensure adequate lighting
- Keep entire hand visible in frame
- Clean camera lens
- Adjust `detectionCon` and `trackCon` values

### Volume Control Not Working
- Ensure you're on Windows OS (Pycaw is Windows-only)
- Run with administrator privileges if needed

## 🚀 Future Enhancements

- [ ] Right-click gesture support
- [ ] Scroll gesture implementation
- [ ] Cross-platform volume control (Mac/Linux)
- [ ] Custom gesture training system
- [ ] Multi-hand support
- [ ] Gesture macro recording
- [ ] Mobile app integration
- [ ] Voice command integration

## 🐛 Known Issues

- Volume control only works on Windows (Pycaw limitation)
- Privacy mode may flicker with very rapid hand movements
- Performance depends heavily on lighting conditions
- Requires adequate camera quality for optimal tracking

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe Team** for the powerful hand tracking framework
- **OpenCV Community** for computer vision tools
- **Python Community** for the robust ecosystem

## 📧 Contact

**Project Link**: [https://github.com/tass027/ai-virtual-mouse](https://github.com/tass027/ai-virtual-mouse)

**Report Issues**: [GitHub Issues](https://github.com/tass027/ai-virtual-mouse/issues)

---

⭐ **If you find this project useful, please give it a star!**