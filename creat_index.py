# create_index.py
from elasticsearch import Elasticsearch

ES_HOST = "https://localhost:9200"
BASIC_AUTH = ("elastic", "VA-OCbn-FfbgUb_7tm_k")
INDEX_NAME = "rag_index"

es = Elasticsearch(
    ES_HOST,
    basic_auth=BASIC_AUTH,
    verify_certs=False,
    ssl_show_warn=False
)

# 1. 定义索引映射（根据你的数据结构调整）
index_mapping = {
    "mappings": {
        "properties": {
            "content": {"type": "text", "analyzer": "ik_max_word"},  # 中文分词（需安装IK插件）
            "title": {"type": "text"},
            "create_time": {"type": "date"}
        }
    }
}

# 2. 创建索引
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=index_mapping)
    print(f"✅ 索引 {INDEX_NAME} 创建成功")
else:
    print(f"ℹ️ 索引 {INDEX_NAME} 已存在，无需重复创建")