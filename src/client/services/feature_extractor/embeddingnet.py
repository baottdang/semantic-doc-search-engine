import torch.nn as nn

class EmbeddingNet(nn.Module):
    def __init__(self, embedding_dim=256):
        import torchvision.models as models

        super().__init__()

        backbone = models.mobilenet_v3_large(pretrained=True)
        self.features = backbone.features

        self.pool = nn.AdaptiveAvgPool2d(1)

        self.embedding = nn.Sequential(
            nn.Linear(960, embedding_dim),  # Change this to 576 if using Mobilenetv3 small, if large use 960
            nn.BatchNorm1d(embedding_dim)
        )

    def forward(self, x):
        import torch.nn.functional as F

        x = self.features(x)
        x = self.pool(x).flatten(1)
        x = self.embedding(x)
        x = F.normalize(x, p=2, dim=1)
        return x