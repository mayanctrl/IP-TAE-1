# Image Resampling and Interpolation Analyzer

A simple Streamlit app made for an Image Processing assignment. It lets you upload
an image, downsample it, and then upsample it back using different interpolation
methods (Nearest Neighbor, Bilinear, Bicubic, Lanczos), comparing the results
using MSE and PSNR.

## How to Install

1. Make sure Python is installed (3.8 or above).
2. Install the required libraries:

```
pip install -r requirements.txt
```

## How to Run

```
streamlit run app.py
```

This will open the app in your browser (usually at http://localhost:8501).

## How to Use

1. Upload an image (jpg/png/bmp).
2. Choose a downsampling factor (2x, 4x, or 8x).
3. Select which interpolation methods you want to compare.
4. View the reconstructed images, their MSE/PSNR values, and the PSNR bar chart.
5. Download any reconstructed image using the download buttons.
