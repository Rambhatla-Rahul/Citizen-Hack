from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from bot_test import analyze_image

app = Flask(__name__)
CORS(app)

# Create a directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate-report', methods=['POST'])
def generate_report():
    # Generate a test report message (optional endpoint)
    report_message = "Hello You!"
    return jsonify({'message': report_message})

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to the uploads directory
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Analyze the image and get the results dictionary
    try:
        analysis_results = analyze_image(file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Optionally delete the file after processing

    return jsonify({'message': 'Image analyzed successfully', 'results': analysis_results}), 200

if __name__ == '__main__':
    app.run(host='192.168.106.190', port=8000)
