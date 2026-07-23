from PySide6 import QtWidgets
from ui.background.background import BackgroundWidget 
from PySide6.QtGui import QFont
import sys

if __name__ == "__main__":    
    app = QtWidgets.QApplication([])

    # Show main window
    app.setFont(QFont("Segoe UI", 11))
    background = BackgroundWidget()
    background.showMaximized()

    sys.exit(app.exec())


