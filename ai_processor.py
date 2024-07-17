from PIL import Image
import cv2
import pytesseract
import numpy as np
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from config import AZURE_VISION_ENDPOINT, AZURE_VISION_KEY
import io
import docx2txt
import requests

class AIProcessor:
    def __init__(self):
        self.computervision_client = ComputerVisionClient(
            AZURE_VISION_ENDPOINT, CognitiveServicesCredentials(AZURE_VISION_KEY)
        )
        # Remove the image_model initialization as it's not used

    def process_file(self, file_path):
        file_extension = file_path.split('.')[-1].lower()
        if file_extension in ['png', 'jpg', 'jpeg', 'bmp']:
            return self._process_image(file_path)
        elif file_extension in ['doc', 'docx']:
            return self._process_document(file_path)
        else:
            return {"error": "Unsupported file type"}

    def _process_image(self, image_path):
        try:
            try:
                image = Image.open(image_path)
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image = Image.open(image_path)
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image = Image.open(image_path).convert("RGB")
            except Exception as e:
                return {
                    "error": f"Failed to open or convert image: {str(e)}",
                    "debug_info": f"Image path: {image_path}, Image mode: {image.mode}, Exception: {str(e)}"
                }
            
            
            try:
                # Image preprocessing using OpenCV and OCR using Tesseract
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

                # OCR using Tesseract
                ocr_text = pytesseract.image_to_string(binary)
                # Generate image description using Azure AI Vision
                image_stream = io.BytesIO()
                image.save(image_stream, format='PNG')
                image_stream.seek(0)

                analysis = self.computervision_client.analyze_image_in_stream(
                    image_stream, visual_features=["Description", "Tags", "Objects", "Categories"]
                )

                # Extract detailed information
                image_description = "No description detected."
                if analysis.description and analysis.description.captions:
                    image_description = analysis.description.captions[0].text

                tags = ", ".join([tag.name for tag in analysis.tags]) if analysis.tags else "No tags detected."
                objects = ", ".join([f"{obj.object_property} (confidence: {obj.confidence:.2f})" for obj in analysis.objects]) if analysis.objects else "No objects detected."
                categories = ", ".join([f"{cat.name} (confidence: {cat.score:.2f})" for cat in analysis.categories]) if analysis.categories else "No categories detected."

                detailed_info = f"Description: {image_description}\nTags: {tags}\nObjects: {objects}\nCategories: {categories}"
                print(f"Detailed image information: {detailed_info}")
                print(f"OCR text: {ocr_text.strip()}")
            except Exception as e:
                return {
                    "error": f"Failed to process OCR: {str(e)}",
                    "debug_info": f"Image path: {image_path}, Image mode: {image.mode}, Exception: {str(e)}"
                }
            
            extracted_info = f"Image Description: {image_description}\nOCR Text: {ocr_text}"
            
            return {
                "extracted_info": extracted_info,
                "image_description": image_description,
                "ocr_text": ocr_text
            }
        except Exception as e:
            print(f"Error processing image: {e}")
            return {
                "error": f"Failed to process image: {str(e)}",
                "extracted_info": "No information could be extracted due to an error.",
                "debug_info": f"Image path: {image_path}"
            }

    def _process_document(self, doc_path):
        text = docx2txt.process(doc_path)
        return {
            "extracted_info": f"Document content:\n{text[:500]}..."  # Limit to first 500 characters
        }

    def generate_scenario(self, criteria, processed_files):
        combined_info = "\n".join([file.get('extracted_info', '') for file in processed_files])
        prompt = f"""Based on the following criteria and extracted information, generate a concise test scenario according to the IEEE 829 standard. Respond in English.

Criteria:
{criteria}

Extracted information:
{combined_info}

Generate a test scenario that:
1. Focuses on key user interface elements and requirements
2. Includes essential test steps
3. Covers main positive and negative test cases
4. Adheres to the IEEE 829 standard
5. Considers main interactions between elements

Test scenario:"""

        # Ensure the prompt is not truncated
        max_prompt_length = 4096  # Adjust this value based on your LLM's maximum input length
        if len(prompt) > max_prompt_length:
            print(f"Warning: Prompt exceeds maximum length. Truncating to {max_prompt_length} characters.")
            prompt = prompt[:max_prompt_length]

        # Send the prompt to the local LLM server
        try:
            print(f"Sending prompt to LLM: {prompt}")
            response = requests.post("http://localhost:1234/v1/completions", json={"prompt": prompt})
            response.raise_for_status()
            response_json = response.json()
            print(f"Full response from LLM: {response_json}")
            scenario = response_json.get("choices", [{}])[0].get("text", "Error: No scenario returned from LLM.")
            print(f"Received scenario from LLM: {scenario}")
            # Remove any extraneous text after the main scenario content
            end_marker = "Test scenario:"
            scenario = scenario.split(end_marker, 1)[-1].strip()
            return scenario
        except requests.RequestException as e:
            print(f"Error generating scenario: {e}")
            return f"Error generating the scenario. Please check if the local LLM is accessible. Debug info: {str(e)}"
