import datetime
import csv
import cv2
import numpy as np
from statistics import mode
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
import os
import time
import tflite_runtime.interpreter as tflite
import glob

def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x
def get_labels(dataset_name):
    if dataset_name == 'fer2013':
        return {0:'angry',1:'disgust',2:'fear',3:'happy',
                4:'sad',5:'surprise',6:'neutral'}
    elif dataset_name == 'imdb':
        return {0:'woman', 1:'man'}
    elif dataset_name == 'KDEF':
        return {0:'AN', 1:'DI', 2:'AF', 3:'HA', 4:'SA', 5:'SU', 6:'NE'}
    else:
        raise Exception('Invalid dataset name')

# parameters for loading data and images
emotion_model_path = 'model.tflite'
emotion_labels = get_labels('fer2013')
# loading models
face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')



interpreter =tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']

# getting input model shapes for inference
#emotion_target_size = emotion_classifier.input_shape[1:3]
emotion_target_size = input_details[0]['shape'][1:3]
# starting lists for calculating modes
emotion_window = []

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)
# Select video or webcam feed
cap = None
USE_WEBCAM = True # If false, loads video file source
if (USE_WEBCAM == True):
    cap = cv2.VideoCapture(0) # Webcam source
else:
    cap = cv2.VideoCapture('./demo/dinner.mp4') # Video file source



# Set default configuration values
sample_time = 1.0
# Add more default values as needed

# Check if configuration file exists
if os.path.exists('config.txt'):
    # Read configuration data from text file
    with open('config.txt', 'r') as f:
        config_data = f.readlines()

    # Parse configuration data
    sample_time = float(config_data[0])
    max_images = int(config_data[2])
    # Add more configuration data as needed
# Add more configuration data as needed

# Set up video capture
#cap = cv2.VideoCapture(0)
start_time_global = time.time()
# Increment frame number
frame_number = 0
max_time = config_data[1]
while cap.isOpened(): # True:
    # Capture frame
    # Check if 10 seconds have passed
    if time.time() - start_time_global > float(max_time):
        break


    ret, bgr_image = cap.read()

    # Perform model inference
    start_time = time.time()

    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    for face_coordinates in faces:

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        # emotion_prediction = emotion_classifier.predict(gray_face)

        input_data = gray_face.astype(np.float32)
        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])

        emotion_prediction = output_data
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)
        print(emotion_text)
        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:
            continue

        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0))
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
        else:
            color = emotion_probability * np.asarray((0, 255, 0))

        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_mode,
                  color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

        inference_time = time.time() - start_time


        # Get current timestamp and detected emotion
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        #emotion_text = 'happy'  # Replace with actual detected emotion
        # Create capturas directory if it does not exist
        if not os.path.exists('capturas'):
            os.makedirs('capturas')
        # Save captured image to file
        
        # Get list of all image files in the capturas folder
        image_files = glob.glob('capturas/*.png')

        # Check if the number of image files exceeds the maximum allowed
        if len(image_files) >= max_images:
            # Get the oldest image file based on creation time
            oldest_image = min(image_files, key=os.path.getctime)
            # Delete the oldest image file
            os.remove(oldest_image)
        filename = f'capturas/{timestamp}_{emotion_text}_{frame_number}.png'
        cv2.imwrite(filename, bgr_image)
        # Increment frame number
        frame_number += 1
        # Write data to CSV file
        with open('output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, emotion_text])

        # Calculate delay based on sample time and inference time
        delay = max(0, sample_time - inference_time)
        time.sleep(delay)

# Release resources
cap.release()
