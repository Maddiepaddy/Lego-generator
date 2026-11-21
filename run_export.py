from image_to_voxels import image_to_voxels
from voxel_to_bricks import voxels_to_lego_bricks
from export_bricks_csv import export_bricks_to_csv

# Path to your test image
image_path = "uploads/horse.jpg"

# Step 1: Convert image to voxels
voxels = image_to_voxels(image_path)

# Step 2: Convert voxels to bricks
bricks = voxels_to_lego_bricks(voxels)

# Step 3: Export to CSV
export_bricks_to_csv(bricks, filename="bricks_output.csv")
print("✅ Export complete! File saved as bricks_output.csv")