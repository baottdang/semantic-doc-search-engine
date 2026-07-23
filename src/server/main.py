from ui.index_manager.index_manager_widget import IndexManagerWindow
from api.api import run_api
from services.db_interface.db_manager import get_db_manager
from PySide6.QtWidgets import QApplication
import threading, sys

if __name__ == "__main__":
    # Starts the api
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    app = QApplication(sys.argv)

    window = IndexManagerWindow()
    window.show()

    sys.exit(app.exec())

    db_manager = get_db_manager()
    db_manager.close_tables()

