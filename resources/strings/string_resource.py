import os, configparser

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

# Watchdog
wdname = "QLenFileWatcherService"
wdpath = r"D:\DEVELOPMENTS\image_and_pdf_search_engine\devspace\src\services\watchdog\watchdog.exe" # placeholder

icon_path = r"D:\DEVELOPMENTS\image_and_pdf_search_engine\devspace\resources\drawables\ql_icon.ico" #placeholder
