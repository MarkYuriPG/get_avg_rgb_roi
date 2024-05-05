import streamlit as st
from PIL import Image
import os

def get_avg_rgb(image_path, roi_fraction):
    image = Image.open(image_path)
    width, height = image.size
    pixels = image.load()

    total_r = 0
    total_g = 0
    total_b = 0
    total_pixels = 0

    # Calculate the dimensions of the ROI based on the fraction of the image size
    roi_width = int(width * roi_fraction)
    roi_height = int(height * roi_fraction)

    # Calculate the starting coordinates of the ROI to center it in the image
    roi_x = (width - roi_width) // 2
    roi_y = (height - roi_height) // 2

    for y in range(roi_y, roi_y + roi_height):
        for x in range(roi_x, roi_x + roi_width):
            pixel = pixels[x, y]
            if len(pixel) >= 3:  # Check if pixel has at least 3 values (RGB)
                r, g, b = pixel[:3]  # Extract RGB values
                total_r += r
                total_g += g
                total_b += b
                total_pixels += 1

    # Check if there are valid pixels in the ROI
    if total_pixels == 0:
        return None  # Return None if there are no valid pixels

    avg_r = total_r / total_pixels
    avg_g = total_g / total_pixels
    avg_b = total_b / total_pixels

    return (avg_r, avg_g, avg_b)


def main():
    st.title("Average RGB of Images")

    # Folder selection
    folder_path = st.sidebar.text_input("Enter folder path:")
    if not folder_path:
        st.warning("Please enter a folder path.")
        return

    # ROI fraction selection
    roi_fraction = st.sidebar.slider("ROI Fraction", min_value=0.1, max_value=1.0, value=0.5, step=0.1)

    # List all files in the folder
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Process each image in the folder
    for image_file in image_files:
        try:
            image_path = os.path.join(folder_path, image_file)
            avg_rgb = get_avg_rgb(image_path, roi_fraction)
            if avg_rgb:
                # Display the image and average RGB values in an expandable section
                with st.expander(f"Image: {image_file}"):
                    # Display the image
                    st.image(image_path, caption="Image", use_column_width=True)
                    # Display the average RGB values
                    st.write(f"**Average RGB value of {image_file}:**")
                    st.write("Red:", avg_rgb[0])
                    st.write("Green:", avg_rgb[1])
                    st.write("Blue:", avg_rgb[2])
            else:
                st.write(f"No valid pixels found in {image_file}.")
        except FileNotFoundError:
            st.error(f"File not found: {image_file}")
        except Exception as e:
            st.error(f"An error occurred while processing {image_file}: {e}")

if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     folder_path = "images"
#     roi_fraction = 0.50  # Adjust the ROI fraction as needed

#     # List all files in the folder
#     image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

#     # Process each image in the folder
#     for image_file in image_files:
#         try:
#             image_path = os.path.join(folder_path, image_file)
#             avg_rgb = get_avg_rgb(image_path, roi_fraction)
#             if avg_rgb:
#                 print(f"Average RGB value of {image_file}:")
#                 print("Red:", avg_rgb[0])
#                 print("Green:", avg_rgb[1])
#                 print("Blue:", avg_rgb[2])
#             else:
#                 print(f"No valid pixels found in {image_file}.")
#         except FileNotFoundError:
#             print(f"File not found: {image_file}")
#         except Exception as e:
#             print(f"An error occurred while processing {image_file}: {e}")