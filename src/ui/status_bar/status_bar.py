from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import ui.index_setup.index_setup_signal as index_signal

class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet('QStatusBar::item {border: None;}')
        self.start_index_label = None
        self.progress_bar = None

        # Connecting signals to slots
        self.index_signal = index_signal.get_index_signal_instance()
        self.index_signal.index_start_signal.connect(self.show_index_constructing)
        self.index_signal.index_complete_signal.connect(self.show_index_complete)

    @Slot()
    def show_index_constructing(self, path):
        self.clearMessage()
        self.start_index_label = QtWidgets.QLabel(f"Constructing {path} index...")
        # Show infinitely loading progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximum(0)
        self.progress_bar.setMinimum(0)

        self.addWidget(self.start_index_label)
        self.addWidget(self.progress_bar)

    @Slot()
    def show_index_complete(self, path, index_name):
        self.removeWidget(self.start_index_label)
        self.removeWidget(self.progress_bar)
        msg = f"Added {path} index successfully to {index_name} index"
        self.show_message(msg, 8000)

    def show_message(self, msg, time=4000):
        self.clearMessage()
        self.showMessage(msg, time)