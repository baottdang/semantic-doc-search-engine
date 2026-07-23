def preprocess(tensor, normalize):
    import torch.nn.functional as F

    # Resize from (3,H,W) → (3,224,224) if not already 224x224
    if tensor.shape[1:] != (224, 224):
        tensor = F.interpolate(
            tensor.unsqueeze(0),  # add batch dim → (1,3,H,W)
            size=(224, 224),
            mode="bilinear",
            align_corners=False
        ).squeeze(0)  # back to (3,224,224)

    # Normalize in-place
    tensor = normalize(tensor)
    return tensor

def preprocess_numpy(array, normalize):
    import numpy as np
    import cv2

    # Ensure dtype is float32
    array = array.astype(np.float32)

    # Resize to (3,224,224) if needed
    if array.shape[1:] != (224, 224):
        # OpenCV expects (H,W,3), so transpose back temporarily
        tmp = np.transpose(array, (1, 2, 0))  # (H,W,3)
        tmp = cv2.resize(tmp, (224, 224), interpolation=cv2.INTER_LINEAR)
        array = np.transpose(tmp, (2, 0, 1))  # back to (3,224,224)

    # Normalize (user-provided function should accept NumPy arrays)
    array = normalize(array)
    return array

def np_array_to_tensor(arr, normalize):
    import torch
    import numpy as np

    if arr is not None:
        # Convert to torch tensor, shape (3, H, W), normalize [0,1]
        if arr.ndim == 2: 
            arr = np.stack([arr]*3, axis=-1)
        tensor = torch.from_numpy(arr).permute(2, 0, 1).float() / 255.0
        # Add batch dimension
        return preprocess(tensor, normalize).unsqueeze(0)
    else:
        return None
    
def process_np_array(np_arr, feature_extractor, device, normalize):
    import torch

    tensor = np_array_to_tensor(np_arr, normalize).to(device)
    with torch.no_grad():
        feats = feature_extractor(tensor)

    return feats.cpu().numpy().astype('float32')

def batch_extract_features(np_arrays, feature_extractor, normalize, TENSOR_BATCH_SIZE=128):
    """
    Process a batch of vectors into feature vectors using the feature extractor model by dividing them into tensor batches.
    
    :param np_arrays: Batch of vectors
    :param feature_extractor: Feature extractor model
    :param normalize: Normalization transform
    """
    import torch
    import numpy as np
    
    tensor_batch_list = []
    for i, np_arr in enumerate(np_arrays, 1):
        if np_arr.ndim == 2: 
            np_arr = np.stack([np_arr]*3, axis=-1)
        tensor = np.transpose(np_arr, (2, 0, 1)).astype(np.float32)
        tensor *= 1.0 / 255.0
        tensor = preprocess_numpy(tensor, normalize)
        tensor_batch_list.append(tensor)  

        if len(tensor_batch_list) == TENSOR_BATCH_SIZE or i == len(np_arrays):
            tensor_batch = np.stack(tensor_batch_list, axis=0)
            with torch.no_grad():
                feats = feature_extractor([tensor_batch])[0]

            del tensor_batch

            yield feats