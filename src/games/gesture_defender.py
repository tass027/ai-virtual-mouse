import cv2
import numpy as np
import pygame
import random
from HandTrackingModule import handDetector

# Initialize Pygame and detector
pygame.init()
detector = handDetector(detectionCon=0.8)
wCam, hCam = 640, 480

# Initialize camera
try:
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
except Exception as e:
    print(f"Camera initialization failed: {str(e)}")
    exit()

# Game setup
gameScreen = pygame.display.set_mode((wCam, hCam))
pygame.display.set_caption("Gesture Defender")

# Game constants
COLORS = {
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "black": (0, 0, 0)
}

# Game entities
gesture_player = pygame.Rect(wCam//2 - 40, hCam-50, 60, 20)
mouse_player = pygame.Rect(wCam//2 + 40, hCam-50, 60, 20)
threats = []
shields = []
gesture_score = 0
mouse_score = 0
game_speed = 5
SPAWN_RATE = 0.05
BASE_SPEED = 5
MAX_GESTURE_SHIELDS = 2
MAX_MOUSE_SHIELDS = 2

# Font setup
font = pygame.font.SysFont("Arial", 30)

def spawn_threat():
    """Spawns a new threat at random X position at top of screen."""
    threats.append({
        "rect": pygame.Rect(random.randint(0, wCam-30), 0, 30, 30),
        "speed": BASE_SPEED + random.randint(-1, 1)
    })

def find_closest_threat(x_pos):
    """Finds the closest threat to a given X position."""
    if not threats:
        return None
    return min(threats, key=lambda t: abs(t['rect'].centerx - x_pos))

def draw_entities():
    """Renders all game elements on screen."""
    gameScreen.fill(COLORS["black"])
    
    # Draw players
    pygame.draw.rect(gameScreen, COLORS["blue"], gesture_player)
    pygame.draw.rect(gameScreen, COLORS["green"], mouse_player)
    
    # Draw threats
    for threat in threats:
        pygame.draw.circle(gameScreen, COLORS["red"], threat['rect'].center, 15)
    
    # Draw shields with owner-based colors
    for shield in shields:
        color = COLORS["yellow"] if shield['owner'] == 'gesture' else COLORS["cyan"]
        pygame.draw.circle(gameScreen, color, shield['rect'].center, 25, 2)
    
    # Score display
    gesture_text = font.render(f"Gesture: {gesture_score}", True, COLORS["blue"])
    mouse_text = font.render(f"Mouse: {mouse_score}", True, COLORS["green"])
    gameScreen.blit(gesture_text, (10, 10))
    gameScreen.blit(mouse_text, (wCam-150, 10))
    
    pygame.display.flip()

try:
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click shooting
                if event.button == 1:
                    closest = find_closest_threat(pygame.mouse.get_pos()[0])
                    if closest:
                        threats.remove(closest)
                        mouse_score += 10
                # Right click shield
                if event.button == 3:
                    mouse_shields = [s for s in shields if s['owner'] == 'mouse']
                    if len(mouse_shields) < MAX_MOUSE_SHIELDS:
                        shields.append({
                            "rect": pygame.Rect(
                                mouse_player.centerx-25,
                                hCam-80,
                                50,
                                50
                            ),
                            "owner": "mouse"
                        })

        # Camera processing
        success, img = cap.read()
        if not success:
            continue
            
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        # Gesture controls
        if len(lmList) >= 21:
            try:
                # Update gesture player position
                gesture_player.centerx = lmList[8][1]

                # Gesture shooting
                if detector.findDistance(8, 12, img)[0] < 40:
                    closest = find_closest_threat(gesture_player.centerx)
                    if closest:
                        threats.remove(closest)
                        gesture_score += 10

                # Gesture shield
                if detector.findDistance(8, 16, img)[0] < 40:
                    gesture_shields = [s for s in shields if s['owner'] == 'gesture']
                    if len(gesture_shields) < MAX_GESTURE_SHIELDS:
                        shields.append({
                            "rect": pygame.Rect(
                                gesture_player.centerx-25,
                                hCam-80,
                                50,
                                50
                            ),
                            "owner": "gesture"
                        })

                # Speed control
                thumb_pinky_dist = detector.findDistance(4, 20, img)[0]
                game_speed = BASE_SPEED + int(thumb_pinky_dist / 25)

            except (IndexError, TypeError):
                pass

        # Mouse position update
        mouse_x, _ = pygame.mouse.get_pos()
        mouse_player.centerx = mouse_x

        # Threat spawning
        if random.random() < SPAWN_RATE:
            spawn_threat()

        # Threat movement and penalty
        for threat in threats[:]:
            threat['rect'].y += threat['speed']
            if threat['rect'].y > hCam:
                # Side-based penalty
                if threat['rect'].x < wCam//2:
                    gesture_score -= 5
                else:
                    mouse_score -= 5
                threats.remove(threat)

        # Shield-threat collision (Corrected Section)
        for shield in shields[:]:
            shield_removed = False
            for threat in threats[:]:
                # Calculate distance between shield and threat centers
                shield_center = shield['rect'].center
                threat_center = threat['rect'].center
                distance = ((shield_center[0] - threat_center[0])**2 + 
                          (shield_center[1] - threat_center[1])**2)**0.5
                if distance < 40:  # Sum of shield (25) and threat (15) radii
                    try:
                        threats.remove(threat)
                    except ValueError:
                        pass  # Threat already removed
                    shield['durability'] = shield.get('durability', 0) + 1
                    if shield['durability'] >= 3:
                        try:
                            shields.remove(shield)
                            shield_removed = True
                        except ValueError:
                            pass
                        break  # Exit threat loop after shield removal
            if shield_removed:
                continue  # Skip further processing for this shield

        draw_entities()
        clock.tick(30)

except KeyboardInterrupt:
    pass
finally:
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()