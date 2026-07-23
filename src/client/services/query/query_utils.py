from PySide6.QtGui import QImage
import numpy as np

def QImageToCvMat(incomingImage):
    rgbimage = incomingImage.convertToFormat(QImage.Format_RGB888)

    width = rgbimage.width()
    height = rgbimage.height()
    bytes_per_line = rgbimage.bytesPerLine()

    ptr = rgbimage.bits()
    arr = np.frombuffer(ptr, np.uint8).reshape((height, bytes_per_line))

    # Slice only the valid pixels (ignore padding)
    arr = arr[:, :width * 3]

    # Reshape into (height, width, 3)
    arr = arr.reshape((height, width, 3))

    # Make contiguous 
    arr = np.ascontiguousarray(arr)

    return arr.copy()

def get_focus(img_arr, focus_thres=0.2):
    """
    Obtain the main focus of the image
    
    :param img_arr: Numpy array of the full image
    """
    from services.object_detection.object_detector import extract_components

    img_arr = img_arr.copy()
    # Extract the components from the image
    components = extract_components(img_arr, kernel_size=3, iteration=3, is_bgr=False)

    # Calculate the full area of the image
    full_area = img_arr.shape[0] * img_arr.shape[1] # Full area of the image

    # Find the component with the largest area
    main_component_nominee = None
    largest_area = 0
    for component in components:
        component_area = component.shape[0] * component.shape[1]
        if component_area > largest_area:
            largest_area = component_area
            main_component_nominee = component

    # Focus on component if its size exceeds the threshold, if not focus on the whole image
    if largest_area / full_area >= focus_thres:
        return main_component_nominee
    
    return img_arr