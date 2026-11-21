import csv
from collections import defaultdict

def generate_brick_summary(filename='bricks_output.csv'):
    brick_counts = defaultdict(int)

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['lego_color'], row['part_id'])
            brick_counts[key] += 1

    print("🧱 Brick Count Summary:")
    for (color, part_id), count in sorted(brick_counts.items(), key=lambda x: -x[1]):
        print(f"- {color} ({part_id}): {count} bricks")

# Run it
if __name__ == '__main__':
    generate_brick_summary()