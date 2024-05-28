from dotenv import load_dotenv
import os
from inference_sdk import InferenceHTTPClient
import supervision as sv
from PIL import Image
import cv2

class DF2_Model:
    def __init__(self):
        load_dotenv()
        self.model = InferenceHTTPClient(
            api_url="https://detect.roboflow.com", api_key=os.getenv("API_KEY")
        )
    
    def infer(self, image):
        results = self.model.infer(image, model_id="deepfashion2-m-10k/2")
        detections = sv.Detections.from_inference(results)
        print(detections)

        def extract_clean_clothing_with_mask(image, mask):
            mask = mask.astype('uint8') * 255
            clean_clothing_region = cv2.bitwise_and(image, image, mask=mask)
            clean_clothing_region = Image.fromarray(cv2.cvtColor(clean_clothing_region, cv2.COLOR_BGR2RGB))
            return clean_clothing_region

        clean_clothing_images = []
        for i, mask in enumerate(detections.mask):
            clean_clothing_region = extract_clean_clothing_with_mask(image, mask)
            clean_clothing_images.append(clean_clothing_region)
        
        return clean_clothing_images
