from PIL import Image, ImageOps

def image_to_voxels(image_path, size=(48, 48)):
    with Image.open(image_path) as image:
        img = ImageOps.exif_transpose(image).convert('RGB')

    img = ImageOps.fit(
        img,
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5)
    )

    pixel_data = img.load()

    voxels = []

    for y in range(size[1]):
        for x in range(size[0]):
            r, g, b = pixel_data[x, y]

            voxel = {
                'x': x,
                'y': y,
                'z': 0,
                'color': (r, g, b)
            }

            voxels.append(voxel)

    return voxels