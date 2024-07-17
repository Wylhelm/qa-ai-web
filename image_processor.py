from PIL import Image
import pytesseract
import io

class ImageProcessor:
    def __init__(self):
        # Initialize image processing libraries here
        tesseract_cmd = shutil.which('tesseract')
        if tesseract_cmd is None:
            raise RuntimeError("Tesseract is not installed or not in the system PATH. Please install Tesseract and make sure it's in your PATH.")
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def process_image(self, image_path):
        # Implement image processing logic here
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        
        # Extract relevant information from the image
        ui_elements = self._extract_ui_elements(text)
        
        # Convert the image to a format that can be stored in the database
        image_data = self._convert_to_database_format(image)
        
        return {
            'ui_elements': ui_elements,
            'image_data': image_data
        }

    def _extract_ui_elements(self, text):
        # Implement logic to extract UI elements from the OCR text
        ui_elements = []
        keywords = ['button', 'input', 'dropdown', 'checkbox', 'radio', 'label', 'text field', 'menu']
        for line in text.split('\n'):
            for keyword in keywords:
                if keyword in line.lower():
                    ui_elements.append(f"{keyword.capitalize()}: {line.strip()}")
                    break
        return ui_elements

    def _convert_to_database_format(self, image):
        # Convert the image to a format that can be stored in the database (e.g., bytes)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return buffered.getvalue()
