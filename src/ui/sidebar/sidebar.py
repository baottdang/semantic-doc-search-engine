from PySide6 import QtWidgets

class SidebarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Layout setup
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)