from flask import Flask, request, jsonify
from flask_cors import CORS

from inference_sdk import InferenceHTTPClient
import numpy as np
import cv2
import supervision as sv
from PIL import Image

import base64
from io import BytesIO
import os
from dotenv import load_dotenv

from models.df1 import DF1_Model

app = Flask(__name__)
CORS(app)

# get the API_KEY from the .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

df1_model = DF1_Model()

@app.route('/api/infer', methods=['POST'])
def infer():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    # Convert the file to an OpenCV image
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # initialize the client
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=API_KEY
    )

    # infer on a local image
    results = CLIENT.infer(image, model_id="deepfashion2-m-10k/2")


    # Load the results into the supervision Detections API
    detections = sv.Detections.from_inference(results)

    # Extract clean clothing regions and return the result
    clean_clothing_images = []
    for i, mask in enumerate(detections.mask):
        clean_clothing_region = extract_clean_clothing_with_mask(image, mask)
        clean_clothing_images.append({
            'image': encode_image_to_base64(clean_clothing_region),
            'attributes': df1_model.predict(Image.fromarray(cv2.cvtColor(clean_clothing_region, cv2.COLOR_BGR2RGB)))
        })

    return jsonify({'clean_clothing_images': clean_clothing_images})

def extract_clean_clothing_with_mask(image, mask):
    mask = mask.astype('uint8') * 255
    clean_clothing_region = cv2.bitwise_and(image, image, mask=mask)
    return clean_clothing_region

def encode_image_to_base64(image):
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
