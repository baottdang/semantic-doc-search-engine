def extract_components(arr, kernel_size=3, is_bgr=True):
    """
    Detect objects within a bitmap, return subarrays of objects
    
    :param arr: Bitmap array
    :param kernel_size: Determines line thickness
    :param is_bgr: Format of image
    """
    import cv2

    # Preprocess the image
    gray_img = cv2.cvtColor(arr , cv2.COLOR_BGR2GRAY if is_bgr else cv2.COLOR_RGB2GRAY) # Assuming that there are only RGB and BGR formats

    # Applying threshold
    threshold = cv2.threshold(gray_img, 150, 255,
        cv2.THRESH_BINARY_INV)[1] 

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    grouped = cv2.dilate(threshold, kernel, iterations=1)

    # Apply the Component analysis function
    analysis = cv2.connectedComponentsWithStats(grouped,
                                                4,
                                                cv2.CV_32S)
    totalLabels, label_ids, values, centroid = analysis

    # Crop the original bitmap into components
    components = []

    for label in range(1, totalLabels):
        x, y, w, h, _ = values[label]

        if h >= 50 and w >= 50:
            cropped = arr[y:y+h, x:x+w]
            components.append(cropped)

    return components