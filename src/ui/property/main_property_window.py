from PySide6 import QtWidgets
from ui.property.default_metadata_panel import DefaultMetadataPanel

class PropertyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()

        self.default_metadata_panel = DefaultMetadataPanel()
        self.custom_metadata_panel = QtWidgets.QWidget()

        self.tabs.addTab(self.default_metadata_panel, "Metadata")
        self.tabs.addTab(self.custom_metadata_panel, "Custom Insight")

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)