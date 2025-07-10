# app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from steganography_core import encode_image, decode_image

st.set_page_config(page_title="Image Steganography with AES", layout="wide")
st.title("🔐 Image Steganography with AES Encryption")

# Custom CSS for better UI
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

menu = ["Encode Message", "Decode Message"]
choice = st.sidebar.selectbox("Choose Action", menu)

if choice == "Encode Message":
    st.header("📤 Encode Message in Image")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            # Display original image
            original_img = Image.open(uploaded_image)
            st.image(original_img, caption="Original Image", use_column_width=True)
            
            # Calculate maximum message length
            img_np = np.array(original_img)
            max_bytes = (img_np.shape[0] * img_np.shape[1] * 3) // 8
            st.info(f"💡 Maximum message length: {max_bytes} characters")
    
    with col2:
        message = st.text_area("Enter the message to hide")
        encryption_key = st.text_input("Enter AES Encryption Key", type="password")
        stego_key = st.text_input("Enter Stego Key", type="password")
        
        # Optional: Custom output filename
        output_filename = st.text_input("Output filename (without extension)", value="output")
        if not output_filename:
            output_filename = "output"
        output_path = f"{output_filename}.png"

    if uploaded_image and message and encryption_key and stego_key:
        try:
            img = Image.open(uploaded_image).convert("RGB")
            img_np = np.array(img)
            capacity = img_np.shape[0] * img_np.shape[1] * 3 // 8

            if capacity < len(message) + len(stego_key):
                st.error(f"❌ Image too small to hold the message and stego key. Maximum capacity: {capacity} characters")
            else:
                with st.spinner("🛠 Encoding in progress..."):
                    encode_image(img_np, message, encryption_key, stego_key, output_path)
                
                # Display encoded image
                encoded_img = Image.open(output_path)
                st.image(encoded_img, caption="Encoded Image", use_column_width=True)
                
                # Add download button
                with open(output_path, "rb") as file:
                    btn = st.download_button(
                        label="📥 Download Encoded Image",
                        data=file,
                        file_name=output_path,
                        mime="image/png"
                    )
                
                st.success("✅ Message encoded successfully!")
                st.info("""
                💡 Important Notes:
                1. The image has been saved as PNG to preserve the hidden data
                2. Use this PNG file for decoding
                3. Keep your stego key and encryption key safe
                4. Do not convert this image to JPG/JPEG
                """)
        except Exception as e:
            st.error(f"❌ Encoding failed: {str(e)}")

elif choice == "Decode Message":
    st.header("📥 Decode Message from Image")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_image = st.file_uploader("Upload stego image", type=["png"])
        if uploaded_image:
            if not uploaded_image.name.lower().endswith('.png'):
                st.error("❌ Please use a PNG file. JPG/JPEG files are not supported as they may corrupt the hidden data.")
                st.stop()
            st.image(uploaded_image, caption="Uploaded Stego Image", use_column_width=True)
    
    with col2:
        stego_key = st.text_input("Enter Stego Key", type="password").strip()
        decryption_key = st.text_input("Enter AES Decryption Key", type="password").strip()

    if uploaded_image and stego_key and decryption_key:
        try:
            img = Image.open(uploaded_image).convert("RGB")
            img_np = np.array(img)
            with st.spinner("🔍 Decoding in progress..."):
                decoded_msg = decode_image(img_np, stego_key, decryption_key)
                if decoded_msg == "❌ Incorrect stego key.":
                    st.error("❌ Incorrect stego key. Please verify the key used during encoding.")
                else:
                    st.success("✅ Decoded Message:")
                    st.code(decoded_msg)
                    # Add copy button
                    st.button("📋 Copy Message", on_click=lambda: st.write(f"<script>navigator.clipboard.writeText('{decoded_msg}')</script>", unsafe_allow_html=True))
        except ValueError as ve:
            st.error(f"❌ Invalid input: {str(ve)}")
        except Exception as e:
            st.error(f"❌ Decoding failed: {str(e)}\nPlease ensure you're using the correct image and keys.")
