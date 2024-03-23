import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import cv2
from keras.models import load_model
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)


model =load_model('BrainTumor10EpochsCategorical.h5')
print('Model loaded. Check http://127.0.0.1:5000/')


def get_className(classNo):
	print(classNo)
	print(classNo[0])
	if classNo[0][0]<1:
		return "This is a Brain Tumor"
	else:
		return "This is not a Brain Tumor"


def getResult(img):
    img = Image.open(image)
    img = img.resize((64, 64))
    img = np.array(img) / 255.0  # Chuẩn hóa ảnh
    img = np.expand_dims(img, axis=0)
    result = model.predict(img)
    return result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            value = getResult(filepath)
            result = get_className(value)
            os.remove(filepath) # remove the file after processing
            return result

    return None

if __name__ == '__main__':
    app.run(debug=True)