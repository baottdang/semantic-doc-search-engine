from PySide6 import QtWidgets
from ui.property.main_property_window import PropertyWindow

class SidebarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Components
        self.property_window = PropertyWindow()

        # Layout setup
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.property_window)
        self.setLayout(self.layout)