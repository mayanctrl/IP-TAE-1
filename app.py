import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Image Resampling and Interpolation Analyzer", layout="wide")

st.title("Image Resampling and Interpolation Analyzer")
st.write("A simple tool to study downsampling, upsampling and interpolation methods (Image Processing Assignment).")

# -----------------------------
# Step 1: Upload Image
# -----------------------------
st.header("1. Upload Image")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    # Read image using PIL then convert to numpy array (RGB)
    pil_img = Image.open(uploaded_file).convert("RGB")
    original_img = np.array(pil_img)

    orig_h, orig_w = original_img.shape[:2]

    st.subheader("Original Image")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(original_img, caption="Original Image", use_container_width=True)
    with col2:
        st.write("**Resolution:**", f"{orig_w} x {orig_h}")
        st.write("**Channels:**", original_img.shape[2])

    # -----------------------------
    # Step 2: Choose downsampling factor
    # -----------------------------
    st.header("2. Choose Downsampling Factor")
    factor = st.selectbox("Downsampling factor", [2, 4, 8])

    new_w = orig_w // factor
    new_h = orig_h // factor

    st.write(f"Image will be downsampled to: **{new_w} x {new_h}**")

    # Downsample using simple area interpolation (like averaging pixels)
    downsampled_img = cv2.resize(original_img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    st.subheader("Downsampled Image")
    st.image(downsampled_img, caption=f"Downsampled ({new_w} x {new_h})", width=300)

    # -----------------------------
    # Step 3: Upsample back using different interpolation methods
    # -----------------------------
    st.header("3. Upsample Back to Original Resolution")

    interpolation_methods = {
        "Nearest Neighbor": cv2.INTER_NEAREST,
        "Bilinear": cv2.INTER_LINEAR,
        "Bicubic": cv2.INTER_CUBIC,
        "Lanczos": cv2.INTER_LANCZOS4
    }

    selected_methods = st.multiselect(
        "Select interpolation methods to compare",
        list(interpolation_methods.keys()),
        default=list(interpolation_methods.keys())
    )

    if len(selected_methods) == 0:
        st.warning("Please select at least one interpolation method.")
    else:
        # -----------------------------
        # Helper functions for MSE and PSNR
        # -----------------------------
        def calculate_mse(img1, img2):
            img1 = img1.astype("float")
            img2 = img2.astype("float")
            mse = np.mean((img1 - img2) ** 2)
            return mse

        def calculate_psnr(mse, max_pixel=255.0):
            if mse == 0:
                return 100.0  # images are identical
            psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
            return psnr

        results = {}      # stores reconstructed images
        mse_values = {}
        psnr_values = {}

        for method_name in selected_methods:
            interp_flag = interpolation_methods[method_name]
            reconstructed = cv2.resize(downsampled_img, (orig_w, orig_h), interpolation=interp_flag)

            mse = calculate_mse(original_img, reconstructed)
            psnr = calculate_psnr(mse)

            results[method_name] = reconstructed
            mse_values[method_name] = mse
            psnr_values[method_name] = psnr

        # -----------------------------
        # Step 4: Display side by side
        # -----------------------------
        st.header("4. Compare Reconstructed Images")

        cols = st.columns(len(selected_methods))
        for col, method_name in zip(cols, selected_methods):
            with col:
                st.image(results[method_name], caption=method_name, use_container_width=True)
                st.write(f"Size: {results[method_name].shape[1]} x {results[method_name].shape[0]}")
                st.write(f"MSE: {mse_values[method_name]:.2f}")
                st.write(f"PSNR: {psnr_values[method_name]:.2f} dB")

        # -----------------------------
        # Step 5: PSNR Table
        # -----------------------------
        st.header("5. MSE and PSNR Table")
        st.write("| Method | MSE | PSNR (dB) |")
        st.write("|---|---|---|")
        for method_name in selected_methods:
            st.write(f"| {method_name} | {mse_values[method_name]:.2f} | {psnr_values[method_name]:.2f} |")

        # -----------------------------
        # Step 6: Bar chart for PSNR
        # -----------------------------
        st.header("6. PSNR Comparison Chart")

        fig, ax = plt.subplots()
        methods_list = list(psnr_values.keys())
        psnr_list = list(psnr_values.values())
        ax.bar(methods_list, psnr_list, color="skyblue")
        ax.set_ylabel("PSNR (dB)")
        ax.set_title("PSNR Comparison of Interpolation Methods")
        plt.xticks(rotation=15)
        st.pyplot(fig)

        # -----------------------------
        # Step 7: Download processed images
        # -----------------------------
        st.header("7. Download Reconstructed Images")

        for method_name in selected_methods:
            img_to_download = Image.fromarray(results[method_name])
            buf = io.BytesIO()
            img_to_download.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label=f"Download {method_name} image",
                data=byte_im,
                file_name=f"{method_name.replace(' ', '_')}_reconstructed.png",
                mime="image/png"
            )

else:
    st.info("Please upload an image to get started.")
