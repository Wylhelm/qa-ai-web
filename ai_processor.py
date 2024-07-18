import docx2txt
import requests
from PyPDF2 import PdfReader
import os
import logging

class AIProcessor:
    def __init__(self):
        self.system_prompt = """You are an AI assistant specialized in generating test scenarios based on given criteria and extracted information from documents. Your task is to create comprehensive test scenarios that adhere to the IEEE 829 standard."""
        self.scenario_prompt = """Based on the following criteria and extracted information, generate a concise test scenario according to the IEEE 829 standard. Respond in English.

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
        self.context_window_size = int(os.getenv('CONTEXT_WINDOW_SIZE', 4096))
        self.llm_endpoint = os.getenv('LLM_ENDPOINT', 'http://localhost:1234/v1/completions')

    def process_file(self, file_path):
        try:
            file_extension = file_path.split('.')[-1].lower()
            if file_extension in ['doc', 'docx']:
                return self._process_word_document(file_path)
            elif file_extension == 'pdf':
                return self._process_pdf_document(file_path)
            elif file_extension == 'txt':
                return self._process_text_file(file_path)
            else:
                return {"error": "Unsupported file type"}
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {str(e)}")
            return {"error": f"Error processing file: {str(e)}"}

    def _process_word_document(self, doc_path):
        text = docx2txt.process(doc_path)
        return {
            "extracted_info": f"Word Document content:\n{text[:500]}..."  # Limit to first 500 characters
        }

    def _process_pdf_document(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return {
            "extracted_info": f"PDF Document content:\n{text[:500]}..."  # Limit to first 500 characters
        }

    def _process_text_file(self, txt_path):
        with open(txt_path, 'r') as file:
            text = file.read()
        return {
            "extracted_info": f"Text File content:\n{text[:500]}..."  # Limit to first 500 characters
        }

    def generate_scenario(self, criteria, processed_files):
        combined_info = "\n".join([file.get('extracted_info', '') for file in processed_files])
        prompt = f"""{self.system_prompt}

{self.scenario_prompt.format(criteria=criteria, combined_info=combined_info)}"""

        max_prompt_length = self.context_window_size
        if len(prompt) > max_prompt_length:
            prompt = prompt[:max_prompt_length]

        try:
            response = requests.post(self.llm_endpoint, json={"prompt": prompt})
            response.raise_for_status()
            response_json = response.json()
            scenario = response_json.get("choices", [{}])[0].get("text", "Error: No scenario returned from LLM.")
            end_marker = "Test scenario:"
            scenario = scenario.split(end_marker, 1)[-1].strip()
            return scenario
        except requests.RequestException as e:
            logging.error(f"Error generating scenario: {str(e)}")
            return f"Error generating the scenario. Please check if the local LLM is accessible. Debug info: {str(e)}"

    # Getter and setter methods remain unchanged
