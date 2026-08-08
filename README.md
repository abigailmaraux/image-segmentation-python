# image-segmentation-python# Python Image Segmentation

A Python-based command-line tool for image processing and object segmentation. This project was developed to isolate objects of interest from their background using binary masks, automatic thresholding, and contour mapping.

## Features
* **Grayscale Conversion & Compression:** Prepares images by converting them to 8-bit grayscale matrices.
* **Gaussian Blur:** Custom implementation to reduce image noise, allowing users to define the radius and sigma.
* **Otsu's Method (Automatic Thresholding):** Analyzes the image histogram to automatically calculate the optimal threshold for binarization.
* **Morphological Transformations:** Includes algorithms for Binary Erosion and Dilation to apply Opening (noise removal) and Closing (hole filling) techniques to the image mask.
* **Contour Mapping:** Overlays a red boundary line on the original image to highlight the segmented objects.
* **Interactive CLI Menu:** A step-by-step interface that guides the user through the segmentation pipeline.

## Technologies & Libraries Used
* **Python 3**
* **NumPy** (Matrix calculations and pixel manipulation)
* **SciPy** (`scipy.ndimage` for advanced filtering)
* **Pillow (PIL)** (Image rendering and formatting)
* **Matplotlib** (Histogram generation and visual output)

## Project Structure
* `main.py` - The entry point of the application that runs the interactive menu.
* `image.py` - Contains the `Image_analysis` class with the core mathematical and algorithmic logic.
* `menu.py` - Handles the command-line interface prompts and user inputs.

## How to Run
Ensure you have the required libraries installed (`pip install numpy scipy pillow matplotlib`). Run the application from your terminal:
```bash
python main.py
