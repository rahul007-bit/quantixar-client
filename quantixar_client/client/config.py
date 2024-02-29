from enum import Enum

class Distance(Enum):
    Manhatten = "Manhatten"
    Euclidean = "Euclidean"
    DotProduct = "DotProduct"
    Cosine = "Cosine"
    Hamming = "Hamming"
    Jaccard = "Jaccard"
    Hellinger = "Hellinger"
    Jeffreys = "Jeffreys"
    JensenShannon = "JensenShannon"

class Config:
    def __init__(self, distance=Distance.Cosine, max_length=16, dim=512):
        self.distance = distance
        self.max_length = max_length
        self.dim = dim

    @classmethod
    def default(cls):
        return cls()
    