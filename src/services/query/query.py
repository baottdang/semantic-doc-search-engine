from services.index.index_construct_utils import get_image_np_arr_scaled
from services.index.feature_extractor.feature_extractor import process_np_array
from services.index.feature_extractor.visionmodel import get_query_vision_model_instance
from PySide6.QtGui import QImage
import numpy as np
import os, cv2

def QImageToCvMat(incomingImage):
    incomingImage = incomingImage.convertToFormat(QImage.Format_RGB888)

    width = incomingImage.width()
    height = incomingImage.height()
    bytes_per_line = incomingImage.bytesPerLine()

    ptr = incomingImage.bits()
    arr = np.frombuffer(ptr, np.uint8).reshape((height, bytes_per_line))

    # Slice only the valid pixels (ignore padding)
    arr = arr[:, :width * 3]

    # Reshape into (height, width, 3)
    arr = arr.reshape((height, width, 3))

    # Make contiguous and convert to BGR for OpenCV
    arr = np.ascontiguousarray(arr)
    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    return arr

def get_focus(img_arr, focus_thres=0.2):
    """
    Obtain the main focus of the image
    
    :param img_arr: Numpy array of the full image
    """
    from services.object_detection.object_detector import extract_components

    # Extract the components from the image
    components = extract_components(img_arr, kernel_size=3, is_bgr=True)

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

def query_path(file_path, index, database, NPROBE=10, NUM_THREAD=2, NUM_RESULTS=10):
    """
    Query the file in the specified index using the file's path
    
    :param file_path: Path to file (image or pdf)
    :param index: Index of the database to search in
    :param NPROBE: Number of clusters to search
    :param NUM_THREAD: Number of threads to perform the query
    :param NUM_RESULTS: Number of returned results
    """
    if not os.path.exists(file_path):
        return []
    vector_arr = get_image_np_arr_scaled(file_path)[0][0][-1] # First page of document

    # Obtain the feature extractor model
    model = get_query_vision_model_instance()
    feature_extractor = model.get_feature_extractor()
    normalize = model.get_normalize()
    feature_vector = process_np_array(vector_arr, feature_extractor, normalize).reshape(1, -1)

    return get_similar_vectors(feature_vector, index, database, NPROBE, NUM_THREAD, NUM_RESULTS)

def query_image(qimage, index, database, NPROBE=150, NUM_THREAD=2, NUM_RESULTS=10):
    """
    Query the image in the specified index using its numpy array
    
    :param qimage: QImage instance of query
    :param index: Index of the database to search in
    :param NPROBE: Number of clusters to search
    :param NUM_THREAD: Number of threads to perform the query
    :param NUM_RESULTS: Number of returned results
    """
    # Obtain the focus of the image
    arr = QImageToCvMat(qimage)
    main_component = get_focus(arr) # Obtain the main focus of the image
    cv2.imwrite("output.png", main_component)
    arr_resized = cv2.resize(main_component, (224, 224), interpolation=cv2.INTER_LINEAR)

    # Obtain the feature extractor model
    model = get_query_vision_model_instance()
    feature_extractor = model.get_feature_extractor()
    normalize = model.get_normalize()

    feature_vector = process_np_array(arr_resized, feature_extractor, normalize).reshape(1, -1)

    return get_similar_vectors(feature_vector, index, database, NPROBE, NUM_THREAD, NUM_RESULTS)

def get_similar_vectors(query, index, database, NPROBE=10, NUM_THREAD=2, NUM_RESULTS=10):
    """
    Query the index for the specified vector, return exact matches and contextually similar vectors along with how similar they are to the source vector
    
    :param query: Query vector
    :param index: Index of the database to search in
    :param database: Database to search in
    :param NPROBE: Number of clusters to search
    :param NUM_THREAD: Number of threads to perform the query
    :param NUM_RESULTS: Number of returned results
    """
    from services.threadlock.threadlock import get_index_rw_lock_instance
    import faiss
    
    results = []
    path_set = set()
    lock_instance = get_index_rw_lock_instance()

    if index:
        index.nprobe = NPROBE
        faiss.omp_set_num_threads(NUM_THREAD)

        # Query with lock
        lock_instance.acquire_read()
        try:
            D, I = index.search(query, k=NUM_RESULTS)
        finally:
            lock_instance.release_read()

        for i, dist in zip(I[0], D[0]):
            data = database.get_index_entry(int(i))
            if data is None:
                continue
            _, _, path, page = data
            if path not in path_set:
                results.append((path, page, dist))
                path_set.add(path)
    
    return results

