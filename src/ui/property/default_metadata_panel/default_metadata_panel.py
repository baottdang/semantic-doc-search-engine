from ui.property.default_metadata_panel.default_metadata_utils import get_metadata_for_display
from ui.property.default_metadata_panel.default_metadata_signal import get_default_metadata_signal_instance
from ui.main_area.gallery_controller.gallery_controller_signal import get_gallery_controller_signal_instance
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6 import QtWidgets

class DefaultMetadataPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Tree View to display the metadata
        self.treeview = QtWidgets.QTreeView()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Tag', 'Info'])

        self.treeview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeview.setModel(self.model)

        # Signal
        self.gallery_controller_signal_instance = get_gallery_controller_signal_instance()
        self.gallery_controller_signal_instance.changed_page_signal.connect(get_metadata_for_display)

        self.default_metadata_panel_signal_instance = get_default_metadata_signal_instance()
        self.default_metadata_panel_signal_instance.metadata_returned_signal.connect(self.display_default_metadata)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.treeview)
        self.setLayout(self.layout)

    def display_default_metadata(self, meta_dict):
        self.model.removeRows(0, self.model.rowCount())
        for tag, value in meta_dict.items():
            tag_item = QStandardItem(tag)
            value_item = QStandardItem(value)
            self.model.appendRow([tag_item, value_item])
