# Import required libraries
import os
from flask import Flask, request, send_file
from flask_cors import CORS
from spleeter.separator import Separator
from pydub import AudioSegment
import chord_detection

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Function to convert WAV to MP3
def convert_to_mp3(input_path, output_path):
    audio = AudioSegment.from_wav(input_path)
    audio.export(output_path, format="mp3")

# Route for file upload and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(filename)

    # Separate stems using Spleeter
    separator = Separator('spleeter:5stems')
    separator.separate_to_file(filename, '/content/')

    # Convert stems to mp3
    stems_path = f'/content/{filename.split(".")[0]}'
    convert_to_mp3(f"{stems_path}/vocals.wav", "vocals.mp3")
    convert_to_mp3(f"{stems_path}/drums.wav", "drums.mp3")
    convert_to_mp3(f"{stems_path}/bass.wav", "bass.mp3")
    convert_to_mp3(f"{stems_path}/other.wav", "keyboard.mp3")
    convert_to_mp3(f"{stems_path}/accompaniment.wav", "guitar.mp3")

    # Process MP3 for chords using the chord detection API
    chords = chord_detection.predict(filename)

    # Placeholder for lyrics extraction
    lyrics = ["Line 1 of lyrics", "Line 2 of lyrics", "Line 3 of lyrics"]  # Replace with actual lyrics extraction logic

    # Combine lyrics and chords into a text file
    with open("lyrics_and_chords.txt", "w") as f:
        for line, chord in zip(lyrics, chords):
            f.write(f"{chord} {line}\n")

    # Create a zip file with all outputs
    os.system(f"zip -r outputs.zip vocals.mp3 drums.mp3 bass.mp3 keyboard.mp3 guitar.mp3 lyrics_and_chords.txt")

    return send_file("outputs.zip", as_attachment=True)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
