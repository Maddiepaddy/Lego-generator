import csv

def export_bricks_to_csv(bricks, filename='bricks_output.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'z', 'brick_type', 'lego_color', 'part_id'])
        for brick in bricks:
            writer.writerow([
                brick['x'],
                brick['y'],
                brick['z'],
                brick['brick_type'],
                brick['lego_color'],
                brick['part_id']
            ])