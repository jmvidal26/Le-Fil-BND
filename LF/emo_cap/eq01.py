import os

#SILENCE THE WARNINGS

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from keras import layers, models
import cv2 as cv
import numpy as np













#==============================================#
#---------------CONFIG-THE-ROUTES--------------#
#==============================================#

#detect EQ01 dir
script_dir= os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join   (script_dir,"dataset")
train_dir = os.path.join   (base_path,"train")
test_dir  = os.path.join   (base_path,"test")
model_path= os.path.join   (base_path,"model_EmotionsRecognitions.h5")

emotions=['angry','happy','neutral','sad']

#PROTECTION VALIDATION
if not os.path.exists(train_dir):
    print(f"The folder train doesn't exists")
    exit()












#=============================================#
#---------------LOAD-DATAset-(^u^)------------#
#=============================================#

print("LOADING...")           #debuging

try:
    #WE LOAD THE FOLDERS

    train_ds= tf.keras.utils.image_dataset_from_directory(train_dir,
        label_mode ='categorical', class_names=emotions,
        color_mode ='grayscale'  , batch_size = 32       ,
        image_size = (64,64))
    
    test_ds= tf.keras.utils.image_dataset_from_directory(test_dir,
        label_mode ='categorical', class_names=emotions,
        color_mode ='grayscale'  , batch_size = 32       ,
        image_size = (64,64)     , shuffle    = False)
    
    print("LOADING ENDS")     #debuging

except ValueError:

    print("'test' EMPTY, USING 20% of train like test")      #debuging

    train_ds, test_ds= tf.keras.utils.image_dataset_from_directory(train_dir,
        validation_split=0.2    , subset      = 'both',
        seed       = 456        , label_mode  = 'categorical',
        class_names= emotions   , color_mode  = 'grayscale'  ,
        batch_size = 32         , image_size  = (64,64))
    
#1st OPTIMIZATION

train_ds= train_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
test_ds =  test_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)












#=============================================#
#-----------------MODEL_CNN--(-_-)------------#
#=============================================#

model= models.Sequential([
    layers.Input(shape=(64, 64, 1))                ,layers.Rescaling   (1./255),

    layers.Conv2D( 32, (3, 3), activation='relu')  ,layers.MaxPooling2D(2, 2)  , 

    layers.Conv2D( 64, (3, 3), activation='relu')  ,layers.MaxPooling2D(2, 2)  ,

    layers.Conv2D(128, (3, 3), activation='relu')  ,layers.MaxPooling2D(2, 2)  ,

    layers.Flatten()                               ,layers.Dropout     (0.5)   ,
    layers.Dense( 128,         activation='relu')  ,
    layers.Dense(len(emotions),activation='softmax')])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])












#=============================================#
#--------------TRAINING-OR-LOAD-(-o-)---------#
#=============================================#

if not os.path.exists(model_path):

    print(f"TRAINING FOR: {emotions}")     #debuging

    model.fit(train_ds, validation_data=test_ds, epochs= 100)
    model.save(model_path)
    local_weights = model.get_weights()

    print(f"MODEL SAVES IN: {model_path}") #debuging

else:

    print("LOADING SAVED MODEL...")       #debuging

    model=models.load_model(model_path)










#=============================================#
#---------------TEST-IN-REAL-TIME-(O_O)-------#
#=============================================#

face_cascade= cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
cap         = cv.VideoCapture(0)

print("\nCAM ACTIVE, PRESS 'j' FOR EXIT") #debuging

while True:

    ret, frame= cap.read()
    if not ret: break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,scaleFactor=2.1,minNeighbors=5)

    for (x, y, w , h) in faces:

        roi_gray  = gray[y:y+h, x:x+w]
        roi_gray  = cv.resize(roi_gray,(64,64))

        img_array = tf.expand_dims(roi_gray ,  0)
        img_array = tf.expand_dims(img_array, -1)

        #PREDICTCS
        preds     = model(img_array, training=False)
        label     = emotions[np.argmax(preds)]

        #DRAW
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv.putText(frame, f"{label}", (x,y-10),
        cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
    cv.imshow("Pseudobrain vision", frame)

    if cv.waitKey(1) & 0xFF == ord('j'): break

cap.release()
cv.destroyAllWindows()