# from PySide6 import QtWidgets
# from ui.background.background import BackgroundWidget
# from services.database.database import get_main_database_instance
# from services.index.index import get_index_instance
# from services.indexer.indexerservice import load_indexer_thread
from services.filewatcherservice.watchdogservice import WatchDog
import resources.strings.string_resource 
# import multiprocessing, sys

if __name__ == "__main__":
    # multiprocessing.freeze_support()
    
    # app = QtWidgets.QApplication([])

    # # Initialize database
    # get_main_database_instance()

    # # Initialize indices
    # get_index_instance()

    # # Start background indexer service
    # load_indexer_thread()

    wd = WatchDog()
    wd.start()

    # # Show main window
    # background = BackgroundWidget()
    # background.showMaximized()

    # sys.exit(app.exec())