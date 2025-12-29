# IMPORTS FOR THIS MODULE MUST BE PUT INSIDE FUNCTIONS, NOT OUTSIDE!
# This is because each global import will be loaded into mem for each process when multiprocessing,
# thus, large imports such as FAISS will be copied over and over unnecessarily, bricking the system. #

def construct_index(folder_path):
    """Construct an index from the files in the given folder path."""
    import os
    import numpy as np
    import faiss
    import time
    import services.index.feature_extractor.visionmodel as vm
    import services.index.index_construct_utils as utils
    import services.index.index_construct_signal as construct_signal
    from itertools import chain
    from concurrent.futures import ProcessPoolExecutor
    from services.database import database as db
    from resources.strings.string_resource import index_path
    from services.index.feature_extractor.feature_extractor import process_np_arrays
    from resources.strings.string_resource import database_path 
    from services.index.index import get_index_instance

    start_time = time.time()

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path {folder_path} does not exist.")
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"The path {folder_path} is not a directory.")
    
    # Get worker's database instance
    database = db.Database(database_path)

    # Create a new index
    nlist = 10  # Number of clusters
    index = utils.create_index(nlist)

    # Bucket to hold entries for batching through yielding
    bucket = []

    index_is_trained = False
    BATCH_SIZE = 1000
    TRAIN_THRESHOLD = nlist * 40  # Number of samples to use for training the index (FAISS' recommendation is >= nlist * 30)
    TENSOR_BATCH_SIZE = utils.get_tensor_batch_size() # Size of tensor batches for feature extraction, MUST NOT BE TOO LARGE SINCE EACH TENSOR TAKES LOTS OF MEM

    # Get vision model instance
    model_inst = vm.get_vision_model_instance()
    feature_extractor = model_inst.get_feature_extractor()
    normalize = model_inst.get_normalize()

    # Get next available index ID 
    next_id = database.get_next_index_id()

    # Get name of index
    index_name = utils.path_to_dbname(folder_path)

    # Loop through each batch of file in the folder tree
    for paths in utils.search_folder_tree(f_address=folder_path, root_level=True, bucket=bucket, BATCH_SIZE=BATCH_SIZE):
        print(len(paths))
        with ProcessPoolExecutor(max_workers=os.cpu_count()//2) as executor:
            np_arr_packages = list(filter(None, executor.map(utils.get_image_np_arr_scaled, paths)))
        
        # If no valid np arrays were returned, skip this batch
        if not np_arr_packages:
            continue

        # Unpack the return package into vectors and paths
        np_arr_tuple, paths = zip(*np_arr_packages)
        np_arrays =  list(chain.from_iterable(np_arr_tuple))

        # Write entries to SQLite metadata db
        ids = []
        for arr_tuples_list, path in zip(np_arr_tuple, paths):
            for page in range(1,len(arr_tuples_list)+1):
                ids.append(next_id)
                database.add_index_entry(next_id, index_name, path, page, commit=False)
                next_id += 1

        # Train and add all features to index
        train_batch = []
        id_ptr = 0
        # Process this batch of vectors into feature vectors, if index isn't trained, train it and add all feature vectors to index 
        for features in process_np_arrays(np_arrays=np_arrays, feature_extractor=feature_extractor, normalize=normalize, TENSOR_BATCH_SIZE=TENSOR_BATCH_SIZE):
            if not index_is_trained:
                train_batch.append(features)
                # If feature vectors exceed the training threshold, train the index
                if sum(f.shape[0] for f in train_batch) >= TRAIN_THRESHOLD:
                    # Concatenate first n samples
                    train_data = np.vstack(train_batch)[:TRAIN_THRESHOLD]
                    index.train(train_data)
                    index_is_trained = True

                    full_buf = np.vstack(train_batch)
                    n = full_buf.shape[0]
                    index.add_with_ids(full_buf, np.array(ids[id_ptr:id_ptr+n], dtype=np.int64))
                    id_ptr += n
                    train_batch.clear()
            else:
                n = features.shape[0]
                index.add_with_ids(features, np.array(ids[id_ptr:id_ptr+n], dtype=np.int64))
                id_ptr += n

    # Write index to disk
    idx_path = os.path.join(index_path, f"{index_name}.index")
    faiss.write_index(index, idx_path)

    # Commit to database
    database.add_database_info(index_name, database_path=folder_path, index_path=idx_path)
    database.commit()
    database.close_connection() # Close the worker's connection to database (The main one is still alive)

    # Update index instance in mem
    index_instance = get_index_instance()
    index_instance.add_new_index_to_mem(index, folder_path)

    # Signal completion
    signal = construct_signal.get_construct_signal_instance()
    signal.construct_complete_signal.emit(folder_path, index_name)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.5f} seconds")