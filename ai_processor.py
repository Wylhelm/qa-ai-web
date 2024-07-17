import docx2txt
import requests
from PyPDF2 import PdfReader

class AIProcessor:
    def __init__(self):
        self.system_prompt = """# *SEARCH/REPLACE block* Rules:

Every *SEARCH/REPLACE block* must use this format:
1. The file path alone on a line, verbatim. No bold asterisks, no quotes around it, no escaping of characters, etc.
2. The opening fence and code language, eg: ```python
3. The start of search block: <<<<<<< SEARCH
4. A contiguous chunk of lines to search for in the existing source code
5. The dividing line: =======
6. The lines to replace into the source code
7. The end of the replace block: >>>>>>> REPLACE
8. The closing fence: ```

Every *SEARCH* section must *EXACTLY MATCH* the existing source code, character for character, including all comments, docstrings, etc.


*SEARCH/REPLACE* blocks will replace *all* matching occurrences.
Include enough lines to make the SEARCH blocks uniquely match the lines to change.

Keep *SEARCH/REPLACE* blocks concise.
Break large *SEARCH/REPLACE* blocks into a series of smaller blocks that each change a small portion of the file.
Include just the changing lines, and a few surrounding lines if needed for uniqueness.
Do not include long runs of unchanging lines in *SEARCH/REPLACE* blocks.

Only create *SEARCH/REPLACE* blocks for files that the user has added to the chat!

To move code within a file, use 2 *SEARCH/REPLACE* blocks: 1 to delete it from its current location, 1 to insert it in the new location.

If you want to put code in a new file, use a *SEARCH/REPLACE block* with:
- A new file path, including dir name if needed
- An empty `SEARCH` section
- The new file's contents in the `REPLACE` section


ONLY EVER RETURN CODE IN A *SEARCH/REPLACE BLOCK*!"""

    def get_system_prompt(self):
        return self.system_prompt

    def set_system_prompt(self, new_prompt):
        self.system_prompt = new_prompt

    def process_file(self, file_path):
        file_extension = file_path.split('.')[-1].lower()
        if file_extension in ['doc', 'docx']:
            return self._process_word_document(file_path)
        elif file_extension == 'pdf':
            return self._process_pdf_document(file_path)
        elif file_extension == 'txt':
            return self._process_text_file(file_path)
        else:
            return {"error": "Unsupported file type"}

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

Based on the following criteria and extracted information, generate a concise test scenario according to the IEEE 829 standard. Respond in English.

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
