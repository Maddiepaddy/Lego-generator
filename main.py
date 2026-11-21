from PIL import Image
from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.utils import secure_filename
from image_to_voxels import image_to_voxels
from voxel_to_bricks import voxels_to_lego_bricks
from export_bricks_csv import export_bricks_to_csv
from visualize_lego import generate_instructions
from collections import Counter
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def generate_parts_list(bricks):
    counts = Counter(
        (brick['brick_type'], brick['lego_color'], brick['part_id'])
        for brick in bricks
    )

    with open('parts_list.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Brick Type', 'Color', 'Part ID', 'Quantity', 'Image URL'])

        for (brick_type, color, part_id), quantity in counts.items():
            writer.writerow([
                brick_type,
                color,
                part_id,
                quantity,
                ''
            ])


@app.route('/')
def home():
    return redirect('/upload-image')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    with Image.open(filepath) as img:
        width, height = img.size

    return jsonify({
        'filename': filename,
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

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        voxels = image_to_voxels(filepath)
        bricks = voxels_to_lego_bricks(voxels)

        export_bricks_to_csv(bricks)
        generate_parts_list(bricks)
        generate_instructions()

        return redirect('/instructions/1')

    return render_template('upload_image.html')


@app.route('/parts')
def show_parts():
    parts = []

    if os.path.exists('parts_list.csv'):
        with open('parts_list.csv', mode='r') as file:
            reader = csv.DictReader(file)
            parts = list(reader)

    return render_template('parts.html', parts=parts)


@app.route('/instructions/<int:step>')
def instructions(step):
    parts = []

    with open('bricks_output.csv', mode='r') as file:
        reader = csv.DictReader(file)
        parts = list(reader)

    step_size = 10
    total_steps = max(1, (len(parts) + step_size - 1) // step_size)

    step = max(1, min(step, total_steps))

    start = (step - 1) * step_size
    end = start + step_size

    current_bricks = parts[start:end]

    return render_template(
        'instructions.html',
        bricks=current_bricks,
        step=step,
        total_steps=total_steps
    )


if __name__ == '__main__':
    app.run(debug=True)
