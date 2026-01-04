from services.index.index_construct_utils import get_image_np_arr_scaled
from services.index.feature_extractor.feature_extractor import process_np_array
from services.index.feature_extractor.visionmodel import get_query_vision_model_instance
from PySide6.QtGui import QImage
import numpy as np
import os

def QImageToCvMat(incomingImage):
    import cv2
    
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

    arr_resized = cv2.resize(arr, (224, 224), interpolation=cv2.INTER_AREA)
    return arr_resized

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
    vector_arr = get_image_np_arr_scaled(file_path)[0][0] # First page of document

    # Obtain the feature extractor model
    model = get_query_vision_model_instance()
    feature_extractor = model.get_feature_extractor()
    normalize = model.get_normalize()
    feature_vector = process_np_array(vector_arr, feature_extractor, normalize).reshape(1, -1)

    return get_similar_vectors(feature_vector, index, database, NPROBE, NUM_THREAD, NUM_RESULTS)

def query_image(qimage, index, database, NPROBE=10, NUM_THREAD=2, NUM_RESULTS=10):
    """
    Query the image in the specified index using its numpy array
    
    :param qimage: QImage instance of query
    :param index: Index of the database to search in
    :param NPROBE: Number of clusters to search
    :param NUM_THREAD: Number of threads to perform the query
    :param NUM_RESULTS: Number of returned results
    """
    # Obtain the feature extractor model
    img_array = QImageToCvMat(qimage)
    model = get_query_vision_model_instance()
    feature_extractor = model.get_feature_extractor()
    normalize = model.get_normalize()

    feature_vector = process_np_array(img_array, feature_extractor, normalize).reshape(1, -1)

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
    import faiss
    
    results = []

    if index:
        index.nprobe = NPROBE
        faiss.omp_set_num_threads(NUM_THREAD)
        D, I = index.search(query, k=NUM_RESULTS)

        for i, dist in zip(I[0], D[0]):
            data = database.get_index_entry(int(i))
            if data is None:
                continue
            _, _, path, page = data
            results.append((path, page, dist))
    
    return results

