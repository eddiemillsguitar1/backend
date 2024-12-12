import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from spleeter.separator import Separator
import tempfile
import shutil
from werkzeug.utils import secure_filename

# Set the environment variable to use Python implementation for protobuf (if not done already)
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Basic route to ensure the app is working
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the MP3 Processing API!"})

# Endpoint to process uploaded MP3 file and return stems
@app.route('/process_mp3', methods=['POST'])
def process_mp3():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Secure the file name and save it temporarily
    filename = secure_filename(file.filename)
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, filename)
    file.save(file_path)
    
    try:
        # Using Spleeter to separate the file into stems
        separator = Separator('spleeter:2stems')  # You can change this to '4stems' or '5stems'
        output_dir = os.path.join(temp_dir, 'output')
        separator.separate_to_file(file_path, output_dir)

        # Find the separated stems
        stems_dir = os.path.join(output_dir, filename.split('.')[0])
        vocals_path = os.path.join(stems_dir, 'vocals.wav')
        accompaniment_path = os.path.join(stems_dir, 'accompaniment.wav')

        # Send the stems back to the client
        return jsonify({
            "vocals": vocals_path,
            "accompaniment": accompaniment_path
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir)

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
