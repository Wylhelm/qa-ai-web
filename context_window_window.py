from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox

class ContextWindowWindow(QDialog):
    def __init__(self, ai_processor):
        super().__init__()
        self.ai_processor = ai_processor
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Select Context Window Size')
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.label = QLabel('Select the context window size:')
        layout.addWidget(self.label)

        self.combo_box = QComboBox()
        self.combo_box.addItem('4096')
        self.combo_box.addItem('8192')
        layout.addWidget(self.combo_box)

        # Set the current index based on the saved value
        current_size = self.ai_processor.get_context_window_size()
        index = self.combo_box.findText(str(current_size))
        if index >= 0:
            self.combo_box.setCurrentIndex(index)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_context_window)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_context_window(self):
        selected_size = int(self.combo_box.currentText())
        self.ai_processor.set_context_window_size(selected_size)
        QMessageBox.information(self, 'Success', f'Context window size set to {selected_size}')
        self.close()
