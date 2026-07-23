# IMPORTS FOR THIS MODULE MUST BE PUT INSIDE FUNCTIONS, NOT OUTSIDE!
# This is because each global import will be loaded into mem for each process when multiprocessing,
# thus, large imports such as FAISS will be copied over and over unnecessarily, bricking the system. #

def construct_index(folder_path):
    """Construct an index from the files in the given folder path."""
    import os
    import time
    import services.index.index_construct_utils as utils
    from resources.strings.string_resource import m, ef_construction, index_model
    from concurrent.futures import ProcessPoolExecutor
    from services.db_interface.database import DatabaseTable
    from services.index.feature_extractor.visionmodel import get_index_vision_model_instance
    from services.index.feature_extractor.feature_extractor import batch_extract_features
    from services.db_interface.db_manager import get_db_manager
    from services.index.index_construct_signal import get_construct_signal_instance

    # Create the database table
    table_name = utils.path_to_dbname(folder_path)
    table = DatabaseTable(table_name, folder_path, index_model)
    db_manager = get_db_manager()

    try:
        start_time = time.time()

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder path {folder_path} does not exist.")
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"The path {folder_path} is not a directory.")
        
        construct_signal_inst = get_construct_signal_instance()

        # Bucket to hold entries for batching through yielding
        bucket = []

        FILE_BATCH_SIZE = 1000
        VECTOR_BATCH_SIZE = 1000
        TENSOR_BATCH_SIZE = utils.get_tensor_batch_size() # Size of tensor batches for feature extraction, MUST NOT BE TOO LARGE SINCE EACH TENSOR TAKES LOTS OF MEM

        # Get vision model instance
        model_inst = get_index_vision_model_instance()
        feature_extractor = model_inst.get_feature_extractor()

        # Loop through each batch of file in the folder tree
        with ProcessPoolExecutor(max_workers=max(1, os.cpu_count() // 2)) as executor:
            for file_paths in utils.search_folder_tree(f_address=folder_path, root_level=True, bucket=bucket, BATCH_SIZE=FILE_BATCH_SIZE):
                # Multiprocessing file vectorization process
                transmit_packet = []
                for np_arr_packages in utils.batch_multiprocess_get_np_scaled(executor, file_paths, VECTOR_BATCH_SIZE=VECTOR_BATCH_SIZE):
                    # If no valid np arrays were returned, skip this batch
                    if not np_arr_packages:
                        continue

                    # Unpack the returned package into vectors and paths
                    file_arr_lists, paths = zip(*np_arr_packages) # Each np_arr_list in np_arr_lists is the list of pages of the file, with each page containing their extracted components
                    # np_arrays = [val for file_list in file_arr_lists for page_list in file_list for val in page_list] # Flattens the list

                    # Extract features and write to database
                    for file_components, path in zip(file_arr_lists, paths):
                        for page_num, page_components in enumerate(file_components):
                            for features in batch_extract_features(np_arrays=page_components, feature_extractor=feature_extractor, normalize=model_inst.normalize, TENSOR_BATCH_SIZE=TENSOR_BATCH_SIZE):
                                for feature in features:
                                    transmit_packet.append((path, page_num, feature))
                table.bulk_insert(transmit_packet)

        # Create index
        table.create_hnsw_index(d_func="vector_l2_ops", m=m, ef_construction=ef_construction)

        # Commit to database
        try:
            table.commit()
        except Exception as e:
            print("Could not write to database")
            return
        # table.close_connection() # Close the worker's connection to database (The main one is still alive)

        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.5f} seconds")

        # Updates the manager
        db_manager.insert_table(table.table_name, table)
        construct_signal_inst.construct_complete_signal.emit(table)

    except Exception as e:
        construct_signal_inst.construct_error_signal.emit(table.folder_path, str(e))



