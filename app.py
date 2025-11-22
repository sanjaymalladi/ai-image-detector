import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Load the model pipeline
# We use the "image-classification" pipeline with the specified model
try:
    print("Loading model...")
    pipe = pipeline("image-classification", model="Ateeqq/ai-vs-human-image-detector")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    pipe = None

@app.route('/')
def home():
    return "AI Image Detector Backend is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    if not pipe:
        return jsonify({"error": "Model not loaded"}), 500

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    try:
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run prediction
        result = pipe(image)
        
        # Result is a list of dicts, e.g., [{'label': 'REAL', 'score': 0.98}, ...]
        # We want to return the most likely label and its score
        top_result = max(result, key=lambda x: x['score'])
        
        return jsonify(top_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
