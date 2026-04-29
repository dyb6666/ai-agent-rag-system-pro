# ES连接 + 向量索引创建
from elasticsearch import Elasticsearch
from config import ES_HOST, CA_CERT_PATH, BASIC_AUTH, VECTOR_DIMS

# 初始化ES客户端
es = Elasticsearch(
    ES_HOST,
    basic_auth=BASIC_AUTH,
    ca_certs=CA_CERT_PATH,
    verify_certs=False,  # 测试环境关闭证书验证
    ssl_show_warn=False
)

def create_vector_index(index_name):
    """创建支持向量检索的ES索引"""
    index_mapping = {
        "mappings": {
            "properties": {
                "content": {"type": "text", "analyzer": "ik_max_word"},  # 中文分词
                "title": {"type": "text"},
                "vector": {  # 向量字段核心配置
                    "type": "dense_vector",
                    "dims": VECTOR_DIMS,
                    "index": True,  # 开启索引支持检索
                    "similarity": "cosine"  # 余弦相似度（推荐）
                }
            }
        }
    }
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_mapping)
        print(f"向量索引 {index_name} 创建成功")
    else:
        print(f"向量索引 {index_name} 已存在")

if __name__ == "__main__":
    from config import INDEX_NAME
    create_vector_index(INDEX_NAME)