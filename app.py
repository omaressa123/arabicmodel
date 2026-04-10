from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import os
import uuid
import sys

# Ensure UTF-8 output for Arabic characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from main import ArabicPresentationGenerator
from arabicmodel.config import DATA_DIR, OUTPUT_DIR

app = Flask(__name__, static_folder='arabicmodel/static', template_folder='arabicmodel/static')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

generator = ArabicPresentationGenerator()

@app.route('/')
def index():
    return render_template('mic.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_audio():
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate unique filename to avoid collisions
    filename = f"record_{uuid.uuid4().hex[:8]}.webm"
    file_path = os.path.join(DATA_DIR, filename)
    audio_file.save(file_path)
    
    print(f"Audio saved to: {file_path}")
    
    try:
        # Run the full pipeline: STT -> Clean -> LLM -> PPTX
        output_pptx = f"presentation_{uuid.uuid4().hex[:8]}.pptx"
        pptx_path = generator.run(file_path, output_pptx)
        
        if pptx_path and os.path.exists(pptx_path):
            return jsonify({
                "success": True,
                "message": "Presentation generated successfully",
                "download_url": f"/download/{os.path.basename(pptx_path)}"
            })
        else:
            return jsonify({"success": False, "error": "Failed to generate presentation"}), 500
            
    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
