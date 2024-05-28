from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np
import cv2

import os
from dotenv import load_dotenv

import base64
from io import BytesIO

from models.df1 import DeepFashion1Model
from models.df2 import DeepFashion2Model

app = Flask(__name__)
CORS(app)

# get the API_KEY from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

df1_model = DeepFashion1Model()
df2_model = DeepFashion2Model()


@app.route("/api/infer", methods=["POST"])
def infer():
    if "file" not in request.files or not request.files["file"]:
        return jsonify({"error": "No file provided"}), 400

    # Convert the file to an OpenCV image
    file_bytes = np.frombuffer(request.files["file"].read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Extract clean clothing regions and return the result
    clean_clothing_images = df2_model.infer(image)

    def encode_image_to_base64(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    response = []
    for clean_clothing_image in clean_clothing_images:
        response.append(
            {
                "image": encode_image_to_base64(clean_clothing_image),
                "attributes": df1_model.infer(clean_clothing_image),
            }
        )

    return jsonify({"body": response})
