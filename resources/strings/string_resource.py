import os, configparser, sys

app_name = "QLen"
version = "2.1.0"
author = "Dang Tran Thai Bao"
filters = "Image files (*.png *.jpg *.jpeg);;Document files (*.pdf *.PDF);;All files (*.png *.jpg *.pdf *.PDF)"
SUPPORTED_IMAGE_FORMATS = (
    ".jpg", ".jpeg", ".png"
)
ALL_SUPPORTED_FORMAT = SUPPORTED_IMAGE_FORMATS + (".pdf",)

home_dir = os.path.expanduser("~") 
index_path = os.path.join(home_dir, "QLenIndex")

# index_path = r"D:\DEVELOPMENTS\QLenIndex" # Testing index_path, comment this and uncomment the one above when cloned to your system

# Ensure index folder always exists
if not os.path.isdir(index_path):
    os.mkdir(index_path)

database_path = os.path.join(index_path, "map_data.db")
journal_path = os.path.join(index_path, "action_journal.db")

# Init config file
config_path = os.path.join(home_dir, "Documents/QLen/config.ini")
os.makedirs(os.path.dirname(config_path), exist_ok=True)
try:
    open(config_path, "x").close()

    # Init config with default settings
    config = configparser.ConfigParser()
    config.read(config_path)

    # Init settings here
    config["filewatcher"] = {"enabled" : False}

    with open(config_path, "w") as f:
        config.write(f)
except FileExistsError:
    pass

# Get anchor location
if getattr(sys, 'frozen', False):  
    # Running as a PyInstaller bundle
    base_path = os.path.dirname(sys.executable)
else:
    # Running in normal Python
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + r"\src" # Quick workaround to getting the main folder's location

# Watchdog
wdname = "QLenFileWatcherService"
wdpath_relative = r"watchdogservice.exe" 
wdpath = os.path.join(base_path, wdpath_relative)

# icon_path = r"drawables\ql_icon.ico" 
icon_path = os.path.join(base_path, r"drawables\ql_icon.ico")

