import csv
from collections import defaultdict

def generate_parts_list(input_file='bricks_output.csv', output_file='parts_list.csv'):
    parts_count = defaultdict(int)

    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['brick_type'], row['lego_color'], row['part_id'])
            parts_count[key] += 1

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Brick Type', 'Color', 'Part ID', 'Quantity', 'Image URL'])

        for (brick_type, color, part_id), count in sorted(parts_count.items(), key=lambda x: -x[1]):
            image_url = f"https://www.bricklink.com/PL/{part_id}.jpg"
            writer.writerow([brick_type, color, part_id, count, image_url])

    print(f"✅ Parts list with image URLs saved to {output_file}")

if __name__ == '__main__':
    generate_parts_list()