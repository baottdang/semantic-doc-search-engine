from services.index.pdfium import pdfium_wrapper
from PySide6.QtGui import QImage, QImageReader
from PySide6.QtCore import QSize
from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS
import cv2, os

def compute_target_size(height, width, viewport_height, viewport_width):
    if height != 0 and width != 0:
        height_scale = viewport_height / height
        width_scale = viewport_width / width
        scale_factor = min(height_scale, width_scale)
        return (int(height * scale_factor), int(width * scale_factor))
    return (0, 0)

def pdf2QImage(file_path, page, viewport_height=0, viewport_width=0, dpi=80):
    """
    Convert a page of the pdf document into QImage object for display purpose
    
    :param file_path: Path to file
    :param page: Page of file
    :param viewport_height: Height of viewport
    :param viewport_width: Width of viewport
    :param dpi: Desired dpi
    """
    if os.path.exists(file_path) and file_path.lower().endswith(".pdf"):
        # Load pdf file to numpy array
        arr_bgra = pdfium_wrapper.render_page_to_numpy(file_path, page - 1, 0, 0, dpi) # Returns in BGRA format
        if arr_bgra is not None:            
            # BGRA → RGB (drops alpha)
            img_bgr = cv2.cvtColor(arr_bgra, cv2.COLOR_BGRA2RGB)

            # Resize to optimal size for viewport
            height, width, _ = img_bgr.shape
            target_height, target_width = compute_target_size(height, width, viewport_height, viewport_width)
            final_width = 0
            final_height = 0

            if target_height != 0 and target_width != 0:
                img_bgr = cv2.resize(img_bgr, (target_width, target_height), interpolation=cv2.INTER_AREA) 
                final_width = target_width
                final_height = target_height
            # Safe fallback
            else: 
                img_bgr = cv2.resize(img_bgr, (width, height), interpolation=cv2.INTER_AREA) 
                final_width = width
                final_height = height

            bytesPerLine = img_bgr.strides[0]
            qimg = QImage(img_bgr.data, final_width, final_height, bytesPerLine, QImage.Format_RGB888).copy()

            return qimg 
    return None

def image2QImage(file_path, viewport_height=0, viewport_width=0):
    """
    Convert an image into QPixmap object for display purpose
    
    :param file_path: Path to file
    :param viewport_height: Height of viewport
    :param viewport_width: Width of viewport
    """
    if os.path.exists(file_path) and file_path.lower().endswith(SUPPORTED_IMAGE_FORMATS):
        reader = QImageReader(file_path)

        # Compute target size
        original_size = reader.size() 
        width = original_size.width() 
        height = original_size.height()
        target_height, target_width = compute_target_size(height, width, viewport_height, viewport_width)
        
        if target_height != 0 and target_width != 0:
            reader.setScaledSize(QSize(target_width, target_height)) 

        qimg = reader.read()
        return qimg.copy()
    return None
