import shutil
from PIL import Image
import pytesseract
import io
import os
import logging

class ImageProcessor:
    def __init__(self):
        tesseract_cmd = os.getenv('TESSERACT_CMD', shutil.which('tesseract'))
        if tesseract_cmd is None:
            logging.error("Tesseract is not installed or not in the system PATH.")
            raise RuntimeError("Tesseract is not installed or not in the system PATH. Please install Tesseract and make sure it's in your PATH.")
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def process_image(self, image_path):
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            ui_elements = self._extract_ui_elements(text)
            image_data = self._convert_to_database_format(image)
            
            return {
                'ui_elements': ui_elements,
                'image_data': image_data
            }
        except Exception as e:
            logging.error(f"Error processing image {image_path}: {str(e)}")
            return {"error": f"Error processing image: {str(e)}"}

    def _extract_ui_elements(self, text):
        ui_elements = []
        keywords = ['button', 'input', 'dropdown', 'checkbox', 'radio', 'label', 'text field', 'menu']
        for line in text.split('\n'):
            for keyword in keywords:
                if keyword in line.lower():
                    ui_elements.append(f"{keyword.capitalize()}: {line.strip()}")
                    break
        return ui_elements

    def _convert_to_database_format(self, image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return buffered.getvalue()
