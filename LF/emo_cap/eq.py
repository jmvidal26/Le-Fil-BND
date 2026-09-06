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

#detect dir
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
#---------------TEST-(O_O)--------------------#
#=============================================#

image_path = os.path.join(script_dir, "processed", "proc_capture_20260906_132157.jpg")
frame = cv.imread(image_path)

if frame is None:
    print(f"Error: Could not load image from {image_path}")
else:
    # Preprocess image: convert to grayscale and resize to (64, 64)
    if len(frame.shape) == 3:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    else:
        gray = frame
    resized = cv.resize(gray, (64, 64))

    # Add batch and channel dimensions: (1, 64, 64, 1)
    img_array = tf.expand_dims(resized, 0)
    img_array = tf.expand_dims(img_array, -1)

    # PREDICTS
    preds = model(img_array, training=False)
    label = emotions[np.argmax(preds.numpy())]

    print(f"Predicted emotion: {label}")
    print(f"Probabilities: {preds.numpy()[0]}")