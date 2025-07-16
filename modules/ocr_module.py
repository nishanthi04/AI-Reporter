import pytesseract
import cv2
import os

# Update with the path to your Tesseract-OCR installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """
    Extracts text from a single image using Tesseract-OCR.
    Args:
        image_path (str): Path to the image file.
    Returns:
        str: Extracted text from the image.
    """
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    text = pytesseract.image_to_string(gray_image)
    return text

def extract_text_from_images(image_folder):
    """
    Extracts text from all images in the specified folder.
    Args:
        image_folder (str): Path to the folder containing images.
    Returns:
        dict: Dictionary where keys are image filenames, and values are extracted texts.
    """
    extracted_texts = {}
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing {image_file}...")
            extracted_texts[image_file] = extract_text_from_image(image_path)
    return extracted_texts

if __name__ == "__main__":
    # Test the OCR module
    test_image_path = "dataset/images/sample_image.jpg"
    print(extract_text_from_image(test_image_path))

    test_folder_path = "dataset/images"
    results = extract_text_from_images(test_folder_path)
    for filename, text in results.items():
        print(f"--- {filename} ---\n{text}\n")
