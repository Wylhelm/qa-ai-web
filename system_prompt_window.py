from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QMessageBox

class SystemPromptWindow(QDialog):
    def __init__(self, ai_processor):
        super().__init__()
        self.ai_processor = ai_processor
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Edit System Prompt')
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlainText(self.ai_processor.get_system_prompt())
        layout.addWidget(self.prompt_edit)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_system_prompt)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_system_prompt(self):
        new_prompt = self.prompt_edit.toPlainText()
        self.ai_processor.set_system_prompt(new_prompt)
        QMessageBox.information(self, 'Success', 'System prompt saved successfully.')
        self.close()
