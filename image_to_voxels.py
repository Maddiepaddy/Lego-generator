from PIL import Image

def image_to_voxels(image_path, size=(32, 32)):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(size)
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