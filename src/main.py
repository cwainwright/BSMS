import sys

from PyQt6.QtWidgets import QApplication

from quickstart import QuickstartWindow

def main():
    app = QApplication(sys.argv)
    quickstart = QuickstartWindow()
    quickstart.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
