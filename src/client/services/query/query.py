from services.np_arr_converter.converter import get_image_np_arr_scaled, resize_and_pad
from services.feature_extractor.feature_extractor import process_np_array
from services.feature_extractor.visionmodel import get_query_vision_model_instance
from services.query.query_utils import get_focus
from services.client.client import get_client
import os

def query_path(file_path, db_path, NUM_RESULTS=15):
    if not os.path.exists(file_path):
        return []
    vector_arr = get_image_np_arr_scaled(file_path) # First page of document
    import cv2
    cv2.imwrite("test.png", cv2.cvtColor(vector_arr, cv2.COLOR_RGB2BGR))

    # Obtain the feature extractor model
    model = get_query_vision_model_instance()
    feature_extractor = model.get_feature_extractor()
    device = model.get_device()

    feature_vector = process_np_array(vector_arr, feature_extractor, device, model.normalize).reshape(1, -1)

    results = get_similar_results(feature_vector, db_path, NUM_RESULTS)
    return results

def query_image(image, db_path, NUM_RESULTS=15):
    # Obtain the focus of the image
    main_component = get_focus(image) # Obtain the main focus of the image, main component is still RGB
    arr_resized = resize_and_pad(main_component)
    print(type(image))

    # Obtain the feature extractor model
    model = get_query_vision_model_instance()
    feature_extractor = model.get_feature_extractor()
    device = model.get_device()

    feature_vector = process_np_array(arr_resized, feature_extractor, device, model.normalize).reshape(1, -1)

    results = get_similar_results(feature_vector, db_path, NUM_RESULTS) # (path, page, embedding)
    
    return results

def get_similar_results(query, db_path, NUM_RESULTS=15):
    client = get_client()
    results = client.query_on_server(query, db_path, NUM_RESULTS)
    return results
