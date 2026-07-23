from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, Qt
from ui.index_manager.index_view.listview_signal import get_listview_signal_instance
from ui.index_manager.index_view.list_action_executor import ListActionExecutor

class CustomListView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Executor
        self.executor = ListActionExecutor()

        # Set custom Menu policy
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)

        # Signal
        self.signal_instance = get_listview_signal_instance()

    def open_menu(self, position: QPoint):
        index = self.indexAt(position)
        if not index.isValid():
            return  # Clicked outside any item

        row = index.row()
        name, path, date_created, index_model = [
            self.model().item(row, col).text()
            for col in range(self.model().columnCount())
        ]

        menu = QtWidgets.QMenu(self)
        action_delete = menu.addAction("Delete this Database")

        action = menu.exec_(self.viewport().mapToGlobal(position)) # Opens the menu at the given screen coordinates and waits until the user selects an action or dismisses the menu

        if action == action_delete:
            if self.confirm_delete(name, path):
                self.model().removeRow(row)

    def confirm_delete(self, name, database_path):
        answer = QtWidgets.QMessageBox.question(
            self,
            'Confirmation',
            f'Permanently remove {database_path} out of database?',
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No
        )
        if answer == QtWidgets.QMessageBox.StandardButton.Yes:
            return self.executor.delete_database(name)
        return False