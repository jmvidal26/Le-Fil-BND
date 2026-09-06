import cv2
import time
import os
from datetime import datetime

#==============================================#
#_______________DATA_RECOLECTION_______________#
#==============================================#

def train():
    base_path = "LF/emo_cap/dataset/train"
    emotions = ['ang', 'hap', 'neu', 'sad']
    for emo in emotions:
        os.makedirs(os.path.join(base_path, emo), exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    print("Controls: 'h'=Happy, 'a'=Angry, 'n'=Neutral, 's'=Sad | 'j' for exit")

    while True:
        ret, frame = cap.read()
        if not ret: break
        

        frame = cv2.flip(frame, 1)
        cv2.imshow('Capture Dataset', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        
        char_key = chr(key) if key != 255 else ''
        
        folder = None
        if char_key == 'h': folder = 'happy'
        elif char_key == 'a': folder = 'angry'
        elif char_key == 'n': folder = 'neutral'
        elif char_key == 's': folder = 'sad'
        
        if folder:
            img_path = os.path.join(base_path, folder, f"user_{count}.jpg")
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(img_path, gray)
            print(f"Foto guardada en {folder}!")
            count += 1
            
        if char_key == 'j':
            break

    cap.release()
    cv2.destroyAllWindows()

CAPTURES_DIR = os.path.join(os.path.dirname(__file__), "captures")
os.makedirs(CAPTURES_DIR, exist_ok=True)







#================================#
#____________eyes_ptr____________#
#================================#


def capture_photo():

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[CAMERA ERROR] No se pudo acceder a la cámara web.")
        return None

    # ilumination...
    time.sleep(90)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("[CAMERA ERROR] No se pudo capturar el fotograma.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    filepath = os.path.join(CAPTURES_DIR, filename)

    cv2.imwrite(filepath, frame)
    print(f"[CAPTURE SUCCESS] Foto tomada y guardada en: {filepath}")
    return filepath





def capture_loop(interval_minutes=20):
    interval_seconds = interval_minutes * 60
    
    try:
        while True:
            capture_photo()
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\nCaptura automática detenida por el usuario.")







if __name__ == "__main__":
    print("Activo")
    capture_photo()