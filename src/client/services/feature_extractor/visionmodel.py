class VisionModel:
    def __init__(self):
        #IMPORTANT!
        # LARGE DEPENDENCIES SUCH AS TORCH MUST BE IMPORTED INSIDE FUNCTIONS
        # THAT GET TOUCHED BY MULTIPROCESSING TO AVOID MEM BLOW UP#
        
        import torch
        import numpy as np
        from resources.strings.string_resource import model_path
        from services.feature_extractor.embeddingnet import EmbeddingNet

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = EmbeddingNet()
        state_dict = torch.load(model_path, map_location=self.device)  
        self.model.load_state_dict(state_dict)                        
        self.model = self.model.to(self.device) 
        self.model.eval()

        self._feature_extractor = self.model

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
_query_vision_model = VisionModel()

def get_query_vision_model_instance():
    return _query_vision_model

