def preprocess(tensor, normalize):
    import torch.nn.functional as F

    # Resize from (3,H,W) → (3,224,224) if not already 224x224
    if tensor[1:].shape != (224, 224):
        tensor = F.interpolate(
            tensor.unsqueeze(0),  # add batch dim → (1,3,H,W)
            size=(224, 224),
            mode="bilinear",
            align_corners=False
        ).squeeze(0)  # back to (3,224,224)

    # Normalize in-place
    tensor = normalize(tensor)
    return tensor

def np_array_to_tensor(arr, normalize):
    import torch

    if arr is not None:
        # Convert to torch tensor, shape (3, H, W), normalize [0,1]
        tensor = torch.from_numpy(arr).permute(2, 0, 1).float() / 255.0
        # Add batch dimension
        return preprocess(tensor, normalize).unsqueeze(0)
    else:
        return None
    
def process_np_array(np_arr, feature_extractor, normalize):
    import torch

    feature_extractor = feature_extractor
    tensor = np_array_to_tensor(np_arr, normalize)
    with torch.no_grad():
        feats = feature_extractor(tensor)

    return feats.numpy().astype('float32')

def process_np_arrays(np_arrays, feature_extractor, normalize, TENSOR_BATCH_SIZE=128):
    """
    Process a batch of vectors into feature vectors using the feature extractor model by dividing them into tensor batches.
    
    :param np_arrays: Batch of vectors
    :param feature_extractor: Feature extractor model
    :param normalize: Normalization transform
    """
    import torch
    
    tensors = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
    feature_extractor = feature_extractor.to(device)
    for i, np_arr in enumerate(np_arrays, 1):
        tensors.append(np_array_to_tensor(np_arr, normalize))
        if len(tensors) == TENSOR_BATCH_SIZE or i == len(np_arrays):
            tensor_batch = torch.cat(tensors, dim=0).to(device)  # shape (B, 3, 224, 224)
            with torch.no_grad():
                feats = feature_extractor(tensor_batch)
            tensors.clear()
            yield feats.cpu().numpy().astype('float32')