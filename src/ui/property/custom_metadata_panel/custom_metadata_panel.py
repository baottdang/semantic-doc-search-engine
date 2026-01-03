from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from ui.property.custom_metadata_panel.custom_metadata_signal import get_custom_metadata_signal_instance
from ui.property.custom_metadata_panel.custom_tree_model import CustomTreeModel, TreeItem
from ui.property.custom_metadata_panel.custom_metadata_controller import CustomMetadataController

class CustomMetadataPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Components
        self.controller = CustomMetadataController()
        self.treeview = QtWidgets.QTreeView()
        self.treeview.setRootIsDecorated(True)

        self.model = CustomTreeModel(TreeItem(["",[]], None))

        self.treeview.setModel(self.model)

        # Signal
        self.custom_metadata_signal_instance = get_custom_metadata_signal_instance()
        self.custom_metadata_signal_instance.done_get_xmp_metadata_signal.connect(self.display_custom_metadata)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.treeview)
        self.setLayout(self.layout)

    def display_custom_metadata(self, meta_dict):
        self.model.removeRows(0, self.model.rowCount())

        # Convert dict to TreeItem
        rootItem = TreeItem(["Custom", meta_dict])
        self.model.set_root(rootItem)