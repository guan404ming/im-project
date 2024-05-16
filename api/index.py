from flask import Flask, request, jsonify
from inference import get_model
import cv2
import numpy as np
import supervision as sv
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

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

    # Load a pre-trained yolov8n model
    model = get_model(model_id="deepfashion2-m-10k/2")

    # Run inference on the image
    results = model.infer(image)[0]

    # Load the results into the supervision Detections API
    detections = sv.Detections.from_inference(results.dict(by_alias=True, exclude_none=True))

    # Extract clean clothing regions and return the result
    clean_clothing_images = []
    for i, mask in enumerate(detections.mask):
        clean_clothing_region = extract_clean_clothing_with_mask(image, mask)
        clean_clothing_images.append(encode_image_to_base64(clean_clothing_region))

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
