class VisionModel:
    def __init__(self):
        #IMPORTANT!
        # LARGE DEPENDENCIES SUCH AS TORCH MUST BE IMPORTED INSIDE FUNCTIONS
        # THAT GET TOUCHED BY MULTIPROCESSING TO AVOID MEM BLOW UP#
        
        import torch
        import numpy as np
        from resources.strings.string_resource import model_path
        import openvino as ov

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.core = ov.Core()

        self.model = self.core.read_model(model_path)

        self._feature_extractor = self.core.compile_model(
            self.model,
            "CPU",
            {}
        )

        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(-1, 1, 1)  # shape (3,1,1)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(-1, 1, 1)    # shape (3,1,1)
            
    def normalize(self, tensor):
        tensor -= self.mean 
        tensor /= self.std
        return tensor
    
    def get_feature_extractor(self):
        return self._feature_extractor
    
    def get_device(self):
        return self.device
    
# Singleton instance of VisionModel
_index_vision_model = None
_query_vision_model = None
_watchdog_vision_model = None

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

def get_watchdog_vision_model_instance():
    global _watchdog_vision_model
    if _watchdog_vision_model is None:
        _watchdog_vision_model = VisionModel()
    return _watchdog_vision_model

