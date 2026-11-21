import math

LEGO_COLORS = {
    "Bright Red": ((180, 0, 0), "3001"),
    "Bright Blue": ((0, 0, 180), "3001"),
    "Bright Yellow": ((255, 205, 0), "3001"),
    "White": ((255, 255, 255), "3001"),
    "Black": ((0, 0, 0), "3001"),
    "Dark Gray": ((100, 100, 100), "3001"),
    "Bright Green": ((0, 200, 0), "3001")
}

def match_color_to_lego(rgb):
    closest_color = None
    min_distance = float('inf')

    for name, (lego_rgb, part_id) in LEGO_COLORS.items():
        distance = math.sqrt(sum((lego_rgb[i] - rgb[i]) ** 2 for i in range(3)))
        if distance < min_distance:
            min_distance = distance
            closest_color = (name, part_id)

    return closest_color