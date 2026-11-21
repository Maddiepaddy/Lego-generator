LEGO_COLORS = {
    "White": (244, 244, 244),
    "Black": (27, 42, 52),
    "Light Bluish Gray": (160, 165, 169),
    "Dark Bluish Gray": (99, 95, 98),
    "Bright Red": (201, 26, 9),
    "Dark Red": (114, 14, 15),
    "Bright Blue": (0, 85, 191),
    "Dark Blue": (10, 52, 99),
    "Medium Blue": (90, 147, 219),
    "Bright Yellow": (242, 205, 55),
    "Bright Green": (75, 159, 74),
    "Dark Green": (0, 69, 26),
    "Lime": (187, 233, 11),
    "Orange": (254, 138, 24),
    "Bright Purple": (200, 112, 160),
    "Lavender": (181, 155, 203),
    "Medium Lavender": (172, 120, 186),
    "Tan": (228, 205, 158),
    "Dark Tan": (149, 138, 115),
    "Reddish Brown": (88, 42, 18),
    "Medium Nougat": (170, 125, 85),
    "Sand Green": (160, 188, 172),
    "Sand Blue": (96, 116, 161),
    "Dark Orange": (169, 85, 0)
}


def match_color_to_lego(rgb):
    closest_color = None
    min_distance = float('inf')

    for name, lego_rgb in LEGO_COLORS.items():
        distance = sum(
            (lego_rgb[i] - rgb[i]) ** 2
            for i in range(3)
        )

        if distance < min_distance:
            min_distance = distance
            closest_color = name

    return closest_color, LEGO_COLORS[closest_color]