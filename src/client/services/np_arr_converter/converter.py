def resize_and_pad(image, target_size: int = 224, margin: int = 12, pad_color=(255, 255, 255)):
    import cv2
    import numpy as np

    h, w = image.shape[:2]

    # Maximum size the resized image can occupy
    usable_size = target_size - 2 * margin

    scale = min(usable_size / w, usable_size / h)

    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))

    # Better interpolation choice
    if scale < 1:
        interp = cv2.INTER_AREA      # Downsample
    else:
        interp = cv2.INTER_CUBIC     # Upsample

    resized = cv2.resize(image, (new_w, new_h), interpolation=interp)

    canvas = np.full(
        (target_size, target_size, 3),
        pad_color,
        dtype=image.dtype,
    )

    x = (target_size - new_w) // 2
    y = (target_size - new_h) // 2

    canvas[y:y + new_h, x:x + new_w] = resized

    return canvas

def imread_unicode(path):
    """
    Read the file like cv2.imread but with Unicode path handling
    
    :param path: Description
    """
    import cv2
    import numpy as np

    with open(path, "rb") as f:
        data = np.frombuffer(f.read(), np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)

def get_image_np_arr_scaled(file, dpi=100):
    """
    Get the vector representation of a file.

    If the file is an image, push it through the image pipeline with cv2, resize with cv2.
    Else if the file is a pdf, render each page with pdfium(C++), resize with cv2.

    Return a package of numpy arrays (for multiple pages) and the file path for synchronization.
    
    :param file: Path to image or pdf file
    """
    # NOTICE : Render a pdf page at native resolution or higher to preserve accuracy in sync with its image counterpart
    import cv2
    from services.np_arr_converter.pdfium import pdfium_wrapper
    from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS

    if file == "":
        return None
    try:
        if file.lower().endswith(SUPPORTED_IMAGE_FORMATS): # If image file
            bgr_arr = imread_unicode(file)
            if bgr_arr is None:
                return None

            page_bgr_arr_re = resize_and_pad(bgr_arr)
            page_np_array = cv2.cvtColor(page_bgr_arr_re, cv2.COLOR_BGR2RGB)
            return page_np_array

        elif file.lower().endswith(".pdf"): # If pdf file
            arr_rgb = pdfium_wrapper.render_doc(file, 0, 0, dpi)[0]

            page_np_array = resize_and_pad(arr_rgb)

            return page_np_array

    except Exception as e:
        print(f"Error with {file}: {e}")
        return None