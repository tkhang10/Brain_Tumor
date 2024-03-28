import os
import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
from PIL import Image
from keras.models import load_model
from flask import Flask, request, render_template
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

    value = get_result(filepath)
    result = get_class_name(value)
    os.remove(filepath)  # remove the file after processing
    return result

if __name__ == '__main__':
    app.run(debug=True)