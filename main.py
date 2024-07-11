import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from ai_processor import AIProcessor
from database import Database
from image_processor import ImageProcessor
from dotenv import load_dotenv

def main():
    load_dotenv()  # Load environment variables from .env file
    app = QApplication(sys.argv)
    ai_processor = AIProcessor()
    database = Database()
    image_processor = ImageProcessor()
    window = MainWindow(ai_processor, database, image_processor)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
