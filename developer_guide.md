# Test Scenario Generator - Developer Guide

## Project Overview 
The Test Scenario Generator is a PyQt5-based desktop application that leverages AI to analyze documents (Word, PDF, and text files) to automatically generate comprehensive test scenarios. It uses natural language processing to create scenarios adhering to the IEEE 829 standard.

## Project Structure
- `main.py`: Entry point of the application
- `gui.py`: Contains the main GUI implementation
- `ai_processor.py`: Handles AI-related operations and scenario generation
- `database.py`: Manages SQLite database operations
- `test_scenario.py`: Defines the TestScenario class
- `config.py`: Contains configuration settings (e.g., Azure AI Vision credentials)

## Setup and Dependencies
1. Ensure Python 3.7+ is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Azure AI Vision and update credentials in `config.py`.
5. Set up a local LLM server (e.g., using LM Studio) accessible at http://localhost:1234.

## Key Components

### MainWindow (gui.py)
- Implements the main application window and user interface.
- Handles user interactions, file uploads, and scenario generation/display.
- Displays the CGI logo.

### AIProcessor (ai_processor.py)
- Processes files (images and documents) using various AI techniques.
- Generates test scenarios using a local LLM server.
- Integrates with Azure AI Vision for image analysis.

### Database (database.py)
- Handles SQLite database operations for storing and retrieving scenarios.
- Implements methods for saving, retrieving, and clearing scenario history.


### TestScenario (test_scenario.py)
- Defines the data structure for test scenarios.
- Implements methods for converting scenarios to/from dictionaries.

## Workflow
1. User creates a new scenario and enters a name.
2. Files are uploaded and processed by `AIProcessor` and `ImageProcessor`.
3. Extracted information is added to the criteria input.
4. User can modify the criteria if needed.
5. `AIProcessor` generates a test scenario based on criteria and processed files using the local LLM server.
6. Generated scenario is displayed, saved to the database, and can be exported.

## Extending the Application
- To add new file types for processing, extend the `process_file` method in `AIProcessor` and create a corresponding processing method.
- To modify the UI, update the `init_ui` method in `MainWindow`.
- To change the database schema, update the `create_table` method in `Database` and adjust related methods.
- To enhance image processing capabilities, modify the `ImageProcessor` class.

## Best Practices
- Follow PEP 8 style guidelines for Python code.
- Write unit tests for new features (use `unittest` or `pytest`).
- Document new methods and classes using docstrings.
- Handle exceptions appropriately and provide user-friendly error messages.
- Use environment variables or a secure method to store sensitive information (e.g., API keys).

## Troubleshooting
- Ensure the local LLM server is running and accessible at http://localhost:1234.
- Check the console output for error messages and stack traces.
- Ensure all required dependencies are installed and up to date.

## Future Improvements
- Implement user authentication and multi-user support.
- Add support for more file formats and AI models.
- Enhance the UI with more interactive features and real-time updates.
- Implement a plugin system for easy extension of file processing capabilities.
- Add a feature to compare and merge multiple scenarios.
- Implement automated testing for the GUI components.
- Improve error handling and user feedback for LLM server connection issues.

For any questions or contributions, please contact the project maintainers.
