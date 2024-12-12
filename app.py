from flask import Flask, request, jsonify
from flask_cors import CORS
from spleeter.separator import Separator
import os
import shutil
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Define a temporary directory for storing uploaded MP3 files and processed stems
UPLOAD_FOLDER = tempfile.mkdtemp()
OUTPUT_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Helper function to check allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle MP3 file upload and stem separation
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the file to separate stems using Spleeter
        separator = Separator('spleeter:2stems')  # Using 2stems (vocals, accompaniment)
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'output')
        separator.separate_to_file(filepath, output_dir)

        # Prepare the output folder (stems) for download
        stem_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                stem_files.append(os.path.join(root, file))

        # Return the paths of stems to the frontend
        return jsonify({'stems': stem_files})

    return jsonify({'error': 'Invalid file type'}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

