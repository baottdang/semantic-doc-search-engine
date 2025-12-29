app_name = "QLen"
version = "1.0.0"
author = "Dang Tran Thai Bao"
filters = "Image files (*.png *.xpm *.jpg);;Document files (*.pdf *.PDF);;All files (*.png *.jpg *.pdf *.PDF)"
SUPPORTED_IMAGE_FORMATS = (
    ".jpg", ".jpeg", ".png"
)
ALL_SUPPORTED_FORMAT = SUPPORTED_IMAGE_FORMATS + (".pdf",)
index_path = r"D:/DEVELOPMENTS/QLenIndex"
database_path = index_path + "/map_data.db"