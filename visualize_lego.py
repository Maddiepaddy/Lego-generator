import csv
import matplotlib.pyplot as plt

# LEGO color name → RGB map
LEGO_RGB_MAP = {
    "Bright Red": (180, 0, 0),
    "Bright Blue": (0, 0, 180),
    "Bright Yellow": (255, 205, 0),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Dark Gray": (100, 100, 100),
    "Bright Green": (0, 200, 0)
}

def visualize_layer_z0(filename='bricks_output.csv'):
    bricks = []
    colors = []

    # Read and filter for z = 0
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['z']) != 0:
                continue  # skip other layers

            x = int(row['x'])
            y = int(row['y'])
            color_name = row['lego_color']
            rgb = LEGO_RGB_MAP.get(color_name, (255, 255, 255))
            bricks.append((x, y))
            colors.append(rgb)

    if not bricks:
        print("No bricks at z = 0")
        return

    # Get grid size
    max_x = max(x for x, y in bricks) + 1
    max_y = max(y for x, y in bricks) + 1
    grid = [[[255, 255, 255] for _ in range(max_x)] for _ in range(max_y)]

    for (x, y), rgb in zip(bricks, colors):
        grid[max_y - y - 1][x] = rgb

    # Plot it
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(grid)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("LEGO Model – Layer Z = 0")
    plt.show()

if __name__ == '__main__':
    visualize_layer_z0()