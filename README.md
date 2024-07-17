# Test Scenario Generator

## Overview
The Test Scenario Generator is an AI-powered desktop application designed to assist testers and QA professionals in creating comprehensive test scenarios. It analyzes documents (Word, PDF, and text files) to generate scenarios that adhere to the IEEE 829 standard.

## Key Features
- Document analysis (Word, PDF, and text files)
- AI-powered test scenario generation
- GUI interface for user interaction
- Scenario history management and storage
- Customizable system and scenario prompts
- Adjustable context window size for AI processing

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
   python main.py
   ```
2. Follow the on-screen instructions to create and generate test scenarios.

## Documentation
- For detailed usage instructions, refer to the [User Guide](user_guide.md).
- For development and contribution guidelines, see the [Developer Guide](developer_guide.md).

## Requirements
- Python 3.7+
- PyQt5
- docx2txt
- PyPDF2
- Pillow
- pytesseract
- Local LLM server (e.g., using LM Studio) accessible at http://localhost:1234

## Contributing
Contributions are welcome! Please read the [Developer Guide](developer_guide.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- CGI for project support
- OpenAI for AI technologies

For more information, please contact the project maintainers.
