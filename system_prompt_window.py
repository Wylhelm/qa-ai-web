from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QMessageBox

class SystemPromptWindow(QDialog):
    def __init__(self, ai_processor, prompt_type):
        super().__init__()
        self.ai_processor = ai_processor
        self.prompt_type = prompt_type
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Edit {self.prompt_type.capitalize()} Prompt')
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.prompt_edit = QTextEdit()
        if self.prompt_type == 'system':
            self.prompt_edit.setPlainText(self.ai_processor.get_system_prompt())
        else:
            self.prompt_edit.setPlainText(self.ai_processor.get_scenario_prompt())
        layout.addWidget(self.prompt_edit)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_prompt)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_prompt(self):
        new_prompt = self.prompt_edit.toPlainText()
        if self.prompt_type == 'system':
            self.ai_processor.set_system_prompt(new_prompt)
            message = 'System prompt saved successfully.'
        else:
            self.ai_processor.set_scenario_prompt(new_prompt)
            message = 'Scenario prompt saved successfully.'
        QMessageBox.information(self, 'Success', message)
        self.close()
