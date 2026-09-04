import cv2
import numpy as np
import os
import glob

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False



CAPTURES_DIR = os.path.join(os.path.dirname(__file__), "captures")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)



#=======================================#
#_____PROCESS_IMG___________XD__________#
#=======================================#



def person_mask(input_shape=(512, 512, 1)):

    if not TF_AVAILABLE:
        return None

    model = models.Sequential([
        layers.Input   (shape=input_shape),
        layers.Conv2D  (       16, (3, 3) , activation='relu', padding='same'),
        layers.MaxPooling2D(       (2, 2)),
        layers.Conv2D      (   32, (3, 3) , activation='relu', padding='same'),
        layers.MaxPooling2D(       (2, 2)),
        layers.Conv2DTranspose(16, (2, 2) , strides=(2, 2)   , padding='same'),
        layers.Conv2DTranspose( 1, (2, 2) , strides=(2, 2)   , padding='same' , activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model



def enhance_shine(gray_img):

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray_img)
 
    enhanced = cv2.convertScaleAbs(enhanced, alpha=1.25, beta=35)
    return enhanced



def process_image(image_path, target_size=(512, 512)):

    img = cv2.imread(image_path)
    if img is None:
        print(f"[PROCESS ERROR]: {image_path}")
        return None

    # 1. Resize (512x512)
    resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # 2. enhance person shine
    enhanced_gray = enhance_shine(gray)

    # 3. Detect...
    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    body_cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'

    mask = np.zeros(target_size, dtype=np.uint8)
    detected_person = False



    if os.path.exists(face_cascade_path):
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
        for (x, y, w, h) in faces:
            detected_person = True
            # Bounding box...
            pad_w = int(w * 1.2)
            pad_h = int(h * 2.5)
            x1, y1 = max(0, x - pad_w), max(0, y - int(h * 0.5))
            x2, y2 = min(target_size[1], x + w + pad_w), min(target_size[0], y + h + pad_h)
            cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

    # Fallback
    if not detected_person:
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        center_region = thresh[128:384, 128:384]
        if np.mean(center_region) < 127:
            thresh = cv2.bitwise_not(thresh)
            
        mask = thresh

    # 4. Mask
    person_only_grayscale = cv2.bitwise_and(enhanced_gray, enhanced_gray, mask=mask)

    # 5. Posprocess
    if TF_AVAILABLE:
        cnn_model = person_mask()
        if cnn_model:
            input_tensor = person_only_grayscale.astype(np.float32) / 255.0
            input_tensor = np.expand_dims(input_tensor, axis=(0, -1))
            
            
            predicted_mask = cnn_model.predict(input_tensor, verbose=0)[0, :, :, 0]
            refined_mask = (predicted_mask > 0.1).astype(np.uint8) * 255
            
        
            if np.sum(refined_mask) > 0:
                person_only_grayscale = cv2.bitwise_and(person_only_grayscale, person_only_grayscale, mask=refined_mask)

    
    filename = "proc_" + os.path.basename(image_path)
    output_path = os.path.join(PROCESSED_DIR, filename)
    cv2.imwrite(output_path, person_only_grayscale)
    print(f"[PROCESS SUCCESS] Imagen procesada (512x512 Escala de Grises - Brillo Aumentado, Persona Aislada) guardada en: {output_path}")
    return output_path



def process_all_captures():
    image_paths = glob.glob(os.path.join(CAPTURES_DIR, "*.jpg")) + glob.glob(os.path.join(CAPTURES_DIR, "*.png"))
    if not image_paths:
        print("[PROCESS LOG] No hay capturas pendientes para procesar.")
        return []

    processed_list = []
    for path in image_paths:
        out = process_image(path)
        if out:
            processed_list.append(out)
    return processed_list



if __name__ == "__main__":
    print("=== MÓDULO DE RECONOCIMIENTO & PROCESAMIENTO DE IMAGEN (CNN + OpenCV) ===")
    process_all_captures()