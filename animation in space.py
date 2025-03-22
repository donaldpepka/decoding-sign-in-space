import moviepy.editor as mp
import os
import re


# Function to extract the numerical part of the filename
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

# Set the directory containing your PNG files
img_dir = 'images/'

# List all PNG files
img_files = [img for img in os.listdir(img_dir) if img.endswith('.png')]

# Sort the files using the custom key function
img_files.sort(key=extract_number)

# Join the sorted filenames with the directory path
img_files = [os.path.join(img_dir, img) for img in img_files]

print(img_files)

# Create a VideoClip from the images
clip = mp.ImageSequenceClip(img_files, fps=30)  # Adjust fps as needed

# Write the VideoClip to a file
clip.write_gif("output.gif")
