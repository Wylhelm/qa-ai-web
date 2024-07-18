# Test Scenario Generator

## Overview
The Test Scenario Generator is an AI-powered web application designed to assist testers and QA professionals in creating comprehensive test scenarios. It analyzes documents (Word, PDF, text files, and images) to generate scenarios that adhere to the IEEE 829 standard.

## Key Features
- Document analysis (Word, PDF, text files, and images)
- AI-powered test scenario generation
- Web-based user interface for easy access
- Scenario history management and storage
- File upload and processing

## Installation
1. Ensure Python 3.7+ is installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/your-repo/test-scenario-generator.git
   ```
3. Navigate to the project directory:
   ```
   cd test-scenario-generator
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python app.py
   ```
2. Open a web browser and navigate to `http://localhost:5000`
3. Follow the on-screen instructions to create and generate test scenarios.

## Requirements
- Python 3.7+
- Flask
- Flask-SQLAlchemy
- docx2txt
- PyPDF2
- Pillow
- pytesseract
- Local LLM server (e.g., using LM Studio) accessible at http://localhost:1234

## Contributing
Contributions are welcome! Please read the contributing guidelines for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License.

## Acknowledgments
- CGI for project support
- OpenAI for AI technologies

For more information, please contact the project maintainers.
