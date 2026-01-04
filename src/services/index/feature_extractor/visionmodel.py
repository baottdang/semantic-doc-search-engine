import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights

class VisionModel:
    def __init__(self):
        self._model = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT)
        self._model.eval()

        # Remove classifier 
        self._feature_extractor = torch.nn.Sequential(
            self._model.features,
            self._model.avgpool,
            torch.nn.Flatten(1)
        )

        self._normalize = transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )

    def get_model(self):
        return self._model
    
    def get_normalize(self):
        return self._normalize
    
    def get_feature_extractor(self):
        return self._feature_extractor
    
# Singleton instance of VisionModel
_index_vision_model = None
_query_vision_model = None

def get_index_vision_model_instance():
    global _index_vision_model
    if _index_vision_model is None:
        _index_vision_model = VisionModel()
    return _index_vision_model

def get_query_vision_model_instance():
    global _query_vision_model
    if _query_vision_model is None:
        _query_vision_model = VisionModel()
    return _query_vision_model

