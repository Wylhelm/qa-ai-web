# Test Scenario Generator - User Guide

## Introduction
The Test Scenario Generator is an AI-powered desktop application designed to assist testers and QA professionals in creating comprehensive test scenarios. It analyzes documents (Word, PDF, and text files) to generate scenarios that adhere to the IEEE 829 standard. This guide will walk you through the main features and how to use the application effectively.

## Getting Started
1. Launch the Test Scenario Generator application.
2. You'll see the main interface with the CGI logo, input areas, buttons, and a scenario history section.

## Creating a New Scenario
1. Click the "Create New Scenario" button at the top of the window.
2. Enter a name for your new scenario when prompted.
3. The scenario name input, criteria input, and file upload button will become enabled.

## Entering Criteria
1. In the criteria text area, enter the requirements, user stories, or any other relevant information for your test scenario.
2. You can modify this information at any time before generating the scenario.

## Uploading Files
1. Click the "Upload Documents (Word/PDF/TXT)" button.
2. Select one or more files (supported formats: DOC, DOCX, PDF, TXT).
3. The application will analyze the files and extract relevant information.
4. Extracted information will be automatically added to the criteria text area.
5. If any errors occur during file analysis, you'll see a warning message with details.

## Customizing Prompts and Context Window
1. Click the "System" button to edit the system prompt used for scenario generation.
2. Click the "Scenario" button to edit the scenario prompt template.
3. Click the "Context Window" button to select the context window size (4096 or 8192 tokens).

## Generating a Test Scenario
1. After entering criteria and uploading files, click the "Generate Test Scenario" button.
2. The application will process your input using a local LLM server and generate a test scenario.
3. The generated scenario will appear in the large text area at the bottom of the window.
4. The scenario will be automatically saved to the database and appear in the scenario history.

## Exporting a Scenario
1. Once a scenario is generated or loaded from history, you can export it by clicking the "Export Scenario" button.
2. Choose a location and filename to save the scenario as a text file.

## Viewing Scenario History
1. The bottom of the window displays a list of previously generated scenarios.
2. Click on any scenario in the list to view its details, including the name, criteria, and generated scenario.
3. The selected scenario's information will be loaded into the main interface for viewing or further editing.

## Clearing Scenario History
1. To remove all saved scenarios, click the "Clear History" button in the scenario history section.
2. Confirm the action when prompted.

## Tips for Best Results
- Provide clear and specific criteria for more accurate scenario generation.
- Include relevant documents that describe the functionality you want to test.
- Review and adjust the automatically extracted information from uploaded files if necessary.

## Troubleshooting
- If file analysis fails, ensure the file is not corrupted and is in a supported format.
- Check the console output or error messages for more detailed information about any issues.
- Verify that all required dependencies are properly installed and configured.
- Ensure that the local LLM server is running and accessible at http://localhost:1234.

## Quitting the Application
- To exit the application, click the "Quit" button at the bottom of the window.

For technical issues or further assistance, please refer to the developer documentation or contact the development team.
