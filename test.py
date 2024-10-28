import streamlit as st
from PIL import Image

def main():
    # Set up the title of the app
    st.title('Image Display Example')

    # File uploader allows user to add their own image
    # uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # if uploaded_file is not None:
        # Open and display the image
    image = Image.open("images/nsw_opal.png")
    st.image(image, caption='Uploaded Image.', use_column_width=True)

if __name__ == "__main__":
    main()