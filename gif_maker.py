from PIL import Image
import os
import re

# Folder containing the images
input_folder = "images/linux"
output_gif = "linux.gif"
frame_duration = 40  # milliseconds between frames

# Regex to match 'generation-<number>.png'
pattern = re.compile(r"generation-(\d+)\.png")

# Collect matching files with their numeric index
image_files = []
for filename in os.listdir(input_folder):
    match = pattern.match(filename)
    if match:
        index = int(match.group(1))
        image_files.append((index, filename))

# Sort and select every 5th image
image_files.sort(key=lambda x: x[0])
sampled_files = [os.path.join(input_folder, f[1]) for i, f in enumerate(image_files) if i % 10 == 0]

# Load frames
frames = [Image.open(path) for path in sampled_files]

# Save to GIF
frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],
    duration=frame_duration,
    loop=0,
    optimize=False
)

print(f"GIF saved as {output_gif} using every 5th frame.")