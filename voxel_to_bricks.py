import csv
from lego_colors import match_color_to_lego

def voxels_to_lego_bricks(voxels):
    """
    Convert voxels into LEGO bricks (1x1 for now) with matched LEGO colors.
    Each voxel becomes a single LEGO brick with position and matched LEGO color.
    """
    bricks = []
    for voxel in voxels:
        color_name, part_id = match_color_to_lego(voxel['color'])
        brick = {
            'x': voxel['x'],
            'y': voxel['y'],
            'z': voxel['z'],
            'brick_type': '1x1',
            'lego_color': color_name,
            'part_id': part_id
        }
        bricks.append(brick)
    return bricks

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
