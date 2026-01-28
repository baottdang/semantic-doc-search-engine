from PySide6 import QtWidgets
from ui.background.background import BackgroundWidget
from services.database import database as db
from services.index import index 
import resources.strings.string_resource 
import multiprocessing, sys
import pyuac

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    app = QtWidgets.QApplication([])

    # Initialize database
    db.get_main_database_instance()

    # Initialize indices
    index.get_index_instance()

    # Show main window
    background = BackgroundWidget()
    background.showMaximized()

    sys.exit(app.exec())