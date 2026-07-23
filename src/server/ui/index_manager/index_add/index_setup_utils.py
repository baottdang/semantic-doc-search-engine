from services.db_interface.db_manager import get_db_manager
from pathlib import Path

def is_child_of_indexed(folder_path):
    """Check if the folder_path is a child of any existing indexed databases."""
    folder_path = Path(folder_path).resolve()
    db_manager = get_db_manager()
    database_paths = db_manager.get_db_paths()
    for path in database_paths:
        db_path = Path(path).resolve()
        if db_path in folder_path.parents: 
            return True
    return False

def is_indexed(folder_path):
    """Check if the folder_path is already indexed."""
    db_manager = get_db_manager()
    return db_manager.is_indexed(folder_path)
