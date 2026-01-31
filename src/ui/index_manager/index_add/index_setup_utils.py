from services.database import database as db
from pathlib import Path
from ui.error.error_signal import get_error_signal_instance

def is_child_of_indexed(folder_path):
    """Check if the folder_path is a child of any existing indexed databases."""
    folder_path = Path(folder_path).resolve()
    database_paths = db.get_main_database_instance().get_indexed_database_paths()
    for path in database_paths:
        db_path = Path(path).resolve()
        if db_path in folder_path.parents: 
            return True
    return False

def is_indexed(folder_path):
    """Check if the folder_path is already indexed."""
    database_paths = db.get_main_database_instance().get_indexed_database_paths()
    return folder_path in database_paths

def done_setup(fut):
    """
    Callback for when adding new index is complete
    
    :param fut: Future instance
    """
    try:
        result = fut.result()  # will raise if construct_index crashed
        print("Task finished with result:", result)
    except Exception as e:
        import traceback
        print("Task raised exception:", e)
        traceback.print_exc()
        error_instance = get_error_signal_instance()
        error_instance.error_signal.emit("Error", f"Error while constructing database\nError message: {e}")



