def search_folder_tree(f_address, root_level=True, bucket=None, BATCH_SIZE=32):
    """
    State of the art recursive folder tree search function that finds matching
    paths in a tree and returns them in batches to avoid memory explosion on
    large trees.

    :param f_address: Path obj to the folder tree
    :param root_level: Bool indicating if it's the root level of recursion
    :param bucket: Bucket to hold entries for batching through yielding
    :param BATCH_SIZE: Size of each batch to yield
    """
    import os
    from resources.strings.string_resource import ALL_SUPPORTED_FORMAT

    child_folders = []

    try:
        with os.scandir(f_address) as files:
            for file in files:
                name = file.name.lower()

                # Skip quotation files
                if name.startswith("quotation "):
                    continue

                if file.is_file() and name.endswith(ALL_SUPPORTED_FORMAT):
                    bucket.append(file.path)
                elif file.is_dir():
                    child_folders.append(file.path)

                if len(bucket) >= BATCH_SIZE:
                    yield bucket[:]
                    bucket.clear()

    except (PermissionError, OSError, FileNotFoundError):
        return

    for folder in child_folders:
        yield from search_folder_tree(
            f_address=folder,
            root_level=False,
            bucket=bucket,
            BATCH_SIZE=BATCH_SIZE,
        )

    if root_level and bucket:
        yield bucket[:]
        bucket.clear()

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
    from services.index.feature_extractor.pdfium import pdfium_wrapper
    from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS
    from services.index.feature_extractor.object_detector import extract_components

    arrays = []
    if file == "":
        return None
    try:
        if file.lower().endswith(SUPPORTED_IMAGE_FORMATS): # If image file
            bgr_arr = imread_unicode(file)
            if bgr_arr is None:
                return None

            # Preprocess each component of an image
            processed_components = []
            for component_arr in extract_components(bgr_arr, is_bgr=True):
                bgr_arr_re = resize_and_pad(component_arr)
                np_array = cv2.cvtColor(bgr_arr_re, cv2.COLOR_BGR2RGB)
                if np_array is not None:
                    processed_components.append(np_array)

            # Include the whole page too
            page_bgr_arr_re = resize_and_pad(bgr_arr)
            page_np_array = cv2.cvtColor(page_bgr_arr_re, cv2.COLOR_BGR2RGB)
            if page_np_array is not None:
                processed_components.append(page_np_array)

            arrays.append(processed_components)

        elif file.lower().endswith(".pdf"): # If pdf file
            for arr_rgb in pdfium_wrapper.render_doc(file, 0, 0, dpi):
                processed_components = []
                if arr_rgb is not None:
                    # Extract components from each page and process
                    for component_arr in extract_components(arr_rgb, is_bgr=False):
                        np_array = resize_and_pad(component_arr)
                        processed_components.append(np_array)     

                # Include the whole page too
                page_np_array = resize_and_pad(arr_rgb)
                processed_components.append(page_np_array)

                arrays.append(processed_components)

    except Exception as e:
        print(f"Error with {file}: {e}")
        return None
    if len(arrays) > 0:
        # Return a tuple of both the vector arrays AND the file path for synchronization
        return (arrays, file)
    else:
        return None

def get_tensor_batch_size():
    """
    Roughly estimate the tensor batch size base on machine's current specs.
    
    """
    import torch, psutil

    if torch.cuda.is_available():
        props = torch.cuda.get_device_properties(0)
        available_vram = props.total_memory / (1024**2) - 2
        if available_vram >= 7.9:
            return 512 # This number works best for some reasons
        else:
            return 256
    else:
        mem = psutil.virtual_memory()
        available_mem = mem.available / (1024**2)
        if available_mem >= 7.9:
            return 512 
        else:
            return 256

def path_to_dbname(path):
    """
    Returns a unique name for database based on its path, where name = base + hash of path
    
    :param path: path to database
    """
    import os, hashlib
    base = os.path.splitext(os.path.basename(path))[0]
    safe_base = "".join(c if c.isalnum() else "_" for c in base)
    hash_suffix = hashlib.md5(path.encode()).hexdigest()[:8]
    return f"{safe_base}_{hash_suffix}"

def batch_multiprocess_get_np_scaled(executor, paths, VECTOR_BATCH_SIZE=1000):
    """
    Batching function to limit the number of extracted np_arrays that exist at once
    
    :param paths: Paths to the files
    :param VECTOR_BATCH_SIZE: Size of the batch
    """
    results = []
    vector_count = 0

    for result in executor.map(get_image_np_arr_scaled, paths):
        if result is None:
            continue

        file_arr_list, path = result

        file_vector_count = sum(len(page) for page in file_arr_list)

        results.append(result)
        vector_count += file_vector_count

        if vector_count >= VECTOR_BATCH_SIZE:
            yield results
            results = []       
            vector_count = 0    
    
    if results:
        yield results