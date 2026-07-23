def extract_components(arr, kernel_size=3, iteration=1, is_bgr=True):
    """
    Detect objects within a bitmap, return subarrays of objects
    
    :param arr: Bitmap array
    :param kernel_size: Determines line thickness
    :param is_bgr: Format of image
    """
    import cv2, numpy as np

    # Preprocess the image
    gray_img = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY if is_bgr else cv2.COLOR_RGB2GRAY) # Assuming that there are only RGB and BGR formats

    sharpness_kernel = np.array([[0, -1, 0], # Sharpen the image to make details stand out
                            [-1, 5, -1],
                            [0, -1, 0]])
    sharpened_img = cv2.filter2D(gray_img, -1, sharpness_kernel)

    # Applying threshold
    threshold = cv2.threshold(sharpened_img, 150, 255,
        cv2.THRESH_BINARY_INV)[1] 

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    grouped = cv2.dilate(threshold, kernel, iterations=iteration)

    # Apply the Component analysis function
    analysis = cv2.connectedComponentsWithStats(grouped,
                                                4,
                                                cv2.CV_32S)
    totalLabels, _, values, _ = analysis

    # Crop the original bitmap into components
    components = []

    for label in range(1, totalLabels):
        x, y, w, h, _ = values[label]

        if h >= 35 and w >= 35:
            cropped = arr[y:y+h, x:x+w].copy()
            components.append(cropped)

    return components