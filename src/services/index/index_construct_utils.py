def search_folder_tree(f_address, root_level=True, bucket=None, BATCH_SIZE=32):
    """
    State of the art recursive folder tree search function that find matching paths in a tree and return them in batches to avoid memory explosion on large trees.
    
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
                if file.is_file() and file.name.lower().endswith(ALL_SUPPORTED_FORMAT):
                    bucket.append(file.path)
                elif file.is_dir():
                    child_folders.append(file.path)

                if len(bucket) >= BATCH_SIZE:
                    yield bucket[:]
                    bucket.clear() 
    except (PermissionError, OSError, FileNotFoundError):
        return  

    for folder in child_folders:
        yield from search_folder_tree(f_address=folder, root_level=False, bucket=bucket, BATCH_SIZE=BATCH_SIZE)

    if root_level and bucket:
        yield bucket[:]
        bucket.clear() 

def create_index(nlist=10, DIMENSION=576):
    """
    Create a new index in mem, currently using FAISS' IndexVFFlat with IndexFlatL2 as quantizer
    
    :param nlist: number of clusters
    :param DIMENSION: dimension of vector
    """
    import faiss

    quantizer = faiss.IndexFlatL2(DIMENSION)
    index = faiss.IndexIVFFlat(quantizer, DIMENSION, nlist, faiss.METRIC_L2)
    return index

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


def get_image_np_arr_scaled(file, dpi=96):
    """
    Get the vector representation of a file.

    If the file is an image, push it through the image pipeline with cv2, resize with cv2.
    Else if the file is a pdf, render each page with pdfium(C++), resize with cv2.

    Return a package of numpy arrays (for multiple pages) and the file path for synchronization.
    
    :param file: Path to image or pdf file
    """
    # NOTICE : Render a pdf page at native resolution or higher to preserve accuracy in sync with its image counterpart
    import cv2
    from services.index.pdfium import pdfium_wrapper
    from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS

    arrays = []
    if file == "":
        return None
    try:
        if file.lower().endswith(SUPPORTED_IMAGE_FORMATS): # If image file
            bgr_arr = imread_unicode(file)
            if bgr_arr is None:
                return None
            bgr_arr_re = cv2.resize(bgr_arr, (224, 224), interpolation=cv2.INTER_LINEAR)
            np_array = cv2.cvtColor(bgr_arr_re, cv2.COLOR_BGR2RGB)
            if np_array is not None:
                arrays.append(np_array)
        elif file.lower().endswith(".pdf"): # If pdf file
            for arr_rgb in pdfium_wrapper.render_doc(file, 0, 0, dpi):
                if arr_rgb is not None:
                    # Drop alpha, convert BGRA → RGB
                    np_array = cv2.resize(arr_rgb, (224, 224), interpolation=cv2.INTER_LINEAR)
                    arrays.append(np_array)          
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

def write_index(index, idx_path):
    """
    Offloader to avoid faiss loading for each process
    
    :param index: Index to write
    :param idx_path: Path to write index
    """
    import faiss
    faiss.write_index(index, idx_path)