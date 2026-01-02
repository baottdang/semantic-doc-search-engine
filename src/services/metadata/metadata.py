from PIL import Image, ExifTags
from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS
import pikepdf
import os

def get_clean_exif(img_path):
    """
    Obtain and filter exif data, discard unreadable byte values
    
    :param img_path: Path to image
    """
    img = Image.open(img_path)
    exif_data = img._getexif()
    if not exif_data:
        return {}

    exif = {}
    for tag, value in exif_data.items():
        # Keep tags that Pillow knows (string names)
        tag_name = ExifTags.TAGS.get(tag)
        if tag_name:
            # Normalize values to strings for display
            if isinstance(value, bytes):
                value = "Unreadable"
            else:
                value = str(value)
            exif[tag_name] = value
    return exif

def get_metadata(path):
    """
    Obtain metadata of file, if pdf use pikepdf, if images use Pillow
    
    :param path: Path to file
    """
    if os.path.exists(path):
        # If file is pdf
        if path.lower().endswith(".pdf"):
            pdf = pikepdf.open(path)
            docinfo = pdf.docinfo
            docinfo_dict = {str(k): str(v) for k, v in docinfo.items()}
            return docinfo_dict
        
        # If file is image
        elif path.lower().endswith(SUPPORTED_IMAGE_FORMATS):
            exif = get_clean_exif(path)
            return exif

    return dict()
