import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from ai_processor import AIProcessor
from database import Database
from image_processor import ImageProcessor
def main():
    app = QApplication(sys.argv)
    ai_processor = AIProcessor()
    database = Database()
    image_processor = ImageProcessor()
    window = MainWindow(ai_processor, database, image_processor)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
