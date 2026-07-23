version = "0.0.1"
app_name = "QLen"
d_model = 256
m=16
ef_construction=128

filters = "Image files (*.png *.jpg *.jpeg);;Document files (*.pdf *.PDF);;All files (*.png *.jpg *.pdf *.PDF)"
SUPPORTED_IMAGE_FORMATS = (
    ".jpg", ".jpeg", ".png"
)
ALL_SUPPORTED_FORMAT = SUPPORTED_IMAGE_FORMATS + (".pdf",)

index_model = "Cad_MobileNetV3_large"

# Credentials (Put this as env var later)
host="localhost"
postgresql_port=5432
server_port=8000
dbname="postgres"
user="postgres"
password="Thaibao2006"


model_path = r"model\cad_mobilenetv3_large.pth"
icon_path = r"resources\drawables\ql_icon.ico"