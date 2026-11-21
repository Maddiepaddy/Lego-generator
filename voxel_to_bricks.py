import csv
from lego_colors import match_color_to_lego


BRICK_TYPES = {
    (2, 4): ("2x4", "3001"),
    (2, 3): ("2x3", "3002"),
    (2, 2): ("2x2", "3003"),
    (1, 4): ("1x4", "3010"),
    (1, 3): ("1x3", "3622"),
    (1, 2): ("1x2", "3004"),
    (1, 1): ("1x1", "3005")
}


def voxels_to_lego_bricks(voxels):
    if not voxels:
        return []

    grid = {}

    for voxel in voxels:
        color_name, _ = match_color_to_lego(voxel['color'])
        grid[(voxel['x'], voxel['y'])] = color_name

    bricks = []
    used = set()

    for y in sorted(set(voxel['y'] for voxel in voxels)):
        for x in sorted(set(voxel['x'] for voxel in voxels)):
            if (x, y) in used:
                continue

            color = grid[(x, y)]

            for (width, height), (brick_type, part_id) in BRICK_TYPES.items():
                positions = [
                    (x + dx, y + dy)
                    for dy in range(height)
                    for dx in range(width)
                ]

                if all(
                    position in grid
                    and position not in used
                    and grid[position] == color
                    for position in positions
                ):
                    bricks.append({
                        'x': x,
                        'y': y,
                        'z': 0,
                        'brick_type': brick_type,
                        'lego_color': color,
                        'part_id': part_id
                    })

                    used.update(positions)
                    break

    return bricks


def export_bricks_to_csv(bricks, filename='bricks_output.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow([
            'x',
            'y',
            'z',
            'brick_type',
            'lego_color',
            'part_id'
        ])

        for brick in bricks:
            writer.writerow([
                brick['x'],
                brick['y'],
                brick['z'],
                brick['brick_type'],
                brick['lego_color'],
                brick['part_id']
            ])