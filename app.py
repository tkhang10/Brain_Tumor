import os
import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
from PIL import Image
from keras.models import load_model
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the pre-trained model
model = load_model('BrainTumor10EpochsCategorical.h5')
print('Model loaded. Check http://127.0.0.1:5000/')

# Function to get class name based on prediction
def get_class_name(classNo):
    if classNo[0][0] < 1:
        return "This is a Brain Tumor"
    else:
        return "This is not a Brain Tumor"

# Function to get prediction result from image
def get_result(filepath):
    img = Image.open(filepath)
    img = img.resize((64, 64))
    img = np.array(img) / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)
    result = model.predict(img)
    return result

# Function to draw tumor box on the image
def draw_tumor_box(image, box_coordinates):
    x1, y1, x2, y2 = box_coordinates
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)  
    return image

# Home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Set the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Prediction route
@app.route('/predict', methods=['POST'])
def upload():
    file = request.files['file']

    if not file:
        return 'No file specified.'

    if not allowed_file(file.filename):
        return 'Invalid file extension. Only PNG, JPG, and JPEG are allowed.'

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file.save(filepath)

    # Get prediction result
    value = get_result(filepath)
    result = get_class_name(value)
    
    if result == "This is a Brain Tumor":

        # Load the image to draw tumor box
        image = cv2.imread(filepath)

        # Example coordinates of the tumor box
        box_coordinates = (100,100,200,200)

        # Draw tumor box on the image
        image_with_tumor = draw_tumor_box(image.copy(), box_coordinates)

        # Save the image with tumor box
        new_filename = 'colorize_' + secure_filename(file.filename)
        image_with_tumor_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        cv2.imwrite(image_with_tumor_path, image_with_tumor)

        # Remove the uploaded file after processing (optional)
        # os.remove(filepath)

        # Return the result and the image
        return render_template('index.html', result=result, image_path=image_with_tumor_path)
    
    else:
        # Return only the result
        return result
    

    
if __name__ == '__main__':
    app.run(debug=True)