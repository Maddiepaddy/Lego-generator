import csv
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from lego_colors import LEGO_COLORS


def generate_instructions(filename='bricks_output.csv', step_size=10):
    bricks = []

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row['z']) == 0:
                width, height = map(int, row['brick_type'].split('x'))

                bricks.append({
                    'x': int(row['x']),
                    'y': int(row['y']),
                    'width': width,
                    'height': height,
                    'color': row['lego_color']
                })

    if not bricks:
        return

    grid_width = max(brick['x'] + brick['width'] for brick in bricks)
    grid_height = max(brick['y'] + brick['height'] for brick in bricks)

    os.makedirs('static', exist_ok=True)

    for filename_in_folder in os.listdir('static'):
        if filename_in_folder.startswith('instructions_step_') and filename_in_folder.endswith('.png'):
            os.remove(os.path.join('static', filename_in_folder))

    total_steps = math.ceil(len(bricks) / step_size)

    for step in range(1, total_steps + 1):
        fig, ax = plt.subplots(figsize=(9, 9))

        ax.set_xlim(0, grid_width)
        ax.set_ylim(grid_height, 0)
        ax.set_aspect('equal')

        ax.set_facecolor('#eeeeee')

        for brick in bricks[:step * step_size]:
            x = brick['x']
            y = brick['y']
            width = brick['width']
            height = brick['height']

            rgb = LEGO_COLORS.get(brick['color'], (200, 200, 200))
            color = tuple(value / 255 for value in rgb)

            rectangle = Rectangle(
                (x, y),
                width,
                height,
                facecolor=color,
                edgecolor='#333333',
                linewidth=0.7
            )

            ax.add_patch(rectangle)

            for dx in range(width):
                for dy in range(height):
                    stud = Circle(
                        (x + dx + 0.5, y + dy + 0.5),
                        radius=0.28,
                        facecolor=color,
                        edgecolor=(0, 0, 0, 0.3),
                        linewidth=0.6
                    )

                    ax.add_patch(stud)

        ax.set_xticks([])
        ax.set_yticks([])

        ax.set_title(
            f'LEGO Building Instructions - Step {step}',
            fontsize=15,
            pad=20
        )

        fig.savefig(
            f'static/instructions_step_{step}.png',
            bbox_inches='tight',
            dpi=120
        )

        plt.close(fig)


if __name__ == '__main__':
    generate_instructions()
