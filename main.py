from PIL import Image
from flask import Flask, request, jsonify, render_template, redirect
import csv
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return "LEGO Builder API is running."

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Placeholder for image processing logic
        img = Image.open(filepath)
        width, height = img.size

        return jsonify({
            'filename': file.filename,
            'dimensions': {'width': width, 'height': height},
            'message': 'Image received successfully.'
        })

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image_form():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Process the image
            from image_to_voxels import image_to_voxels
            from voxel_to_bricks import voxels_to_lego_bricks
            from export_bricks_csv import export_bricks_to_csv

            voxels = image_to_voxels(filepath)
            bricks = voxels_to_lego_bricks(voxels)
            export_bricks_to_csv(bricks)

            return redirect('/instructions/1')
    return render_template('upload_image.html')

@app.route('/parts')
def show_parts():
    parts = []
    with open('parts_list.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            parts.append(row)
    return render_template('parts.html', parts=parts)

@app.route('/instructions/<int:step>')
def instructions(step):
    parts = []
    with open('bricks_output.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            parts.append(row)

    step_size = 10
    total_steps = (len(parts) + step_size - 1) // step_size
    step = max(1, min(step, total_steps))
    start = (step - 1) * step_size
    end = start + step_size
    current_bricks = parts[start:end]

    return render_template('instructions.html', bricks=current_bricks, step=step, total_steps=total_steps)

if __name__ == '__main__':
    app.run(debug=True)
