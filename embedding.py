# 向量模型
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed_text(text: str):

    vector = model.encode(text)

    return vector.tolist()
