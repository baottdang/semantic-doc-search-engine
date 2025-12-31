import os

app_name = "QLen"
version = "1.0.0"
author = "Dang Tran Thai Bao"
filters = "Image files (*.png *.xpm *.jpg);;Document files (*.pdf *.PDF);;All files (*.png *.jpg *.pdf *.PDF)"
SUPPORTED_IMAGE_FORMATS = (
    ".jpg", ".jpeg", ".png"
)
ALL_SUPPORTED_FORMAT = SUPPORTED_IMAGE_FORMATS + (".pdf",)

# home_dir = os.path.expanduser("~") 
# index_path = os.path.join(home_dir, "QLenIndex")

index_path = r"D:\DEVELOPMENTS\QLenIndex" # Testing index_path, comment this and uncomment the one above when cloned to your system

# Ensure index folder always exists
if not os.path.isdir(index_path):
    os.mkdir(index_path)

database_path = os.path.join(index_path, "map_data.db")