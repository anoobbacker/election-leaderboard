import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def apply_netflix_style_illustration(image_path, output_path):
    # Step 1: Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    # Step 2: Apply bilateral filter to smooth while keeping edges
    smoothed = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # Step 3: Convert to grayscale and apply median blur
    gray = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 7)

    # Step 4: Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, blockSize=9, C=2)

    # Step 5: Combine edges with the smoothed image
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(smoothed, edges_colored)

    # Step 6: Adjust colors for an artistic effect using PIL
    pil_image = Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Color(pil_image)
    vibrant_image = enhancer.enhance(1.5)

    enhancer = ImageEnhance.Contrast(vibrant_image)
    vibrant_image = enhancer.enhance(1.2)

    # Step 7: Save the result
    vibrant_image.save(output_path)
    print(f"Artistic illustration saved to: {output_path}")

def batch_process_netflix_style_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            apply_netflix_style_illustration(input_path, output_path)

# Example usage
batch_process_netflix_style_images('static/images/candidate.orig', 'netflix_style_candidate_photos')
