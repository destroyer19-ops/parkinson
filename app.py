import os
from flask import request, jsonify
# import tensorflow as tf
# print(tf.__version__)
from config import app
from utils import classify_image, preprocess_image

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

@app.route('/')
def index():
    return "Brain Disease Diagnosis API"

@app.route("/api/classify", methods=["POST"])  # Changed from /classify to /api/classify
def classify():
    try:
        # Changed from "xray_image" to "brain_scan" to match frontend
        if "brain_scan" not in request.files:
            return jsonify({
                "success": False,
                "error": "No file part"
            }), 400
        
        brain_scan = request.files["brain_scan"]  # Changed variable name
        
        if brain_scan.filename == '':
            return jsonify({
                "success": False,
                "error": "No selected file"
            }), 400
        
        # Process the image
        img_array = preprocess_image(brain_scan)
        classification_result = classify_image(img_array)
        
        # Format response to match frontend expectations
        response = {
            "success": True,
            "data": {
                "classification": classification_result["classification"],
                "confidence": max(
                    classification_result["Alzheimer"],
                    classification_result["Normal"], 
                    classification_result["Parkinson"]
                ),
                "probabilities": {
                    "alzheimers": classification_result["Alzheimer"],
                    "normal": classification_result["Normal"],
                    "parkinsons": classification_result["Parkinson"]
                }
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Processing failed: {str(e)}"
        }), 500

if __name__ == "__main__":
    # Use the PORT environment variable set by Render, default to 5000 if not set
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
