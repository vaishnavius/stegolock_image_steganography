🕵️‍♂️ Steganography Web App
A web-based tool to hide and extract secret messages in images using Streamlit.

🔍 Overview
This project is a web application that allows users to perform image steganography—the art of hiding secret messages within ordinary image files. Built with Streamlit, this app provides a clean and user-friendly interface to securely embed and extract hidden text from PNG images.

✨ Features
🔐 Hide Text in Images: Embed secret messages into PNG files without noticeable changes.

🔎 Extract Hidden Messages: Easily retrieve encoded text from steganographically altered images.

🖼️ PNG Image Support: Works exclusively with PNG format for best quality and consistency.

👨‍💻 User-Friendly Interface: Built using Streamlit for simplicity and quick interaction.

⚙️ Real-Time Encoding/Decoding: All operations are performed in real-time in the browser.

🚀 Getting Started
🔧 Installation
Clone the repository:
- git clone  https://github.com/vaishnavius/stegolock_image_steganography.git
- cd steganography-app  
- Install the required dependencies:
- pip install -r requirements.txt 
- Run the application:
- streamlit run app.py  
🧪 Usage
Encode a Message:

Upload a PNG image.

Enter your secret message.

Download the new image with the hidden message.

Decode a Message:

Upload the previously encoded image.

Click to extract the hidden message.

📦 Requirements
Python 3.7+

Streamlit

OpenCV

NumPy

Pillow (PIL)

📁 Folder Structure (optional section)
Copy
Edit
steganography-app/  
├── app.py  
├── utils/  
│   └── stego_utils.py  
├── requirements.txt  
└── README.md  

