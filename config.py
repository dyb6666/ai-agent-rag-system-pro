# 配置
ES_HOST = "https://localhost:9200"
CA_CERT_PATH = "D:/elasticsearch-8.19.10/config/certs/http_ca.crt"
BASIC_AUTH = ("elastic", "VA-OCbn-FfbgUb_7tm_k")
INDEX_NAME = "rag_vector_index3"  # 新的向量索引名

# 向量模型配置
EMBEDDING_MODEL = "BAAI/bge-base-zh"
VECTOR_DIMS = 768  # bge-base-zh输出维度
TOP_K = 3  # 向量检索返回条数

# LLM配置
OPENAI_API_KEY = "sk-52268b1f4f5b4afba95dd3b48a05b933"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"