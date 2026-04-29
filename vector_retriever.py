# 基于向量相似度的检索
import numpy as np
from elasticsearch import NotFoundError
from embedding import embed_text
from es_client import es
from config import INDEX_NAME, TOP_K

# 新增：检索调优参数（可放入config.py）
EF_SEARCH = 200  # HNSW检索参数（越大越准，建议100-500）
NUM_CANDIDATES = 50  # 候选集大小（建议为TOP_K的5-10倍）
VECTOR_NORM = True  # 是否对向量归一化（必须和文档向量保持一致）

def normalize_vector(vector):
    """
    向量归一化（关键：解决余弦相似度计算偏差）
    :param vector: 原始向量列表
    :return: 归一化后的向量
    """
    if not vector or len(vector) == 0:
        return []
    # 转换为numpy数组计算（更高效）
    vec_np = np.array(vector, dtype=np.float32)
    # 计算L2范数
    norm = np.linalg.norm(vec_np)
    if norm == 0:
        return vector
    # 归一化
    normalized_vec = (vec_np / norm).tolist()
    return normalized_vec

def vector_search(question, top_k=None, ef_search=None, num_candidates=None):
    """
    优化版：问题向量化 → 向量归一化 → ES向量余弦相似度检索
    :param question: 用户问题
    :param top_k: 自定义返回条数（默认用配置值）
    :param ef_search: HNSW检索参数（默认用配置值）
    :param num_candidates: 候选集大小（默认用配置值）
    :return: 按相似度排序的检索结果
    """
    # 使用默认参数（方便灵活调优）
    top_k = top_k or TOP_K
    ef_search = ef_search or EF_SEARCH
    num_candidates = num_candidates or NUM_CANDIDATES

    # 1. 问题向量化
    query_vector = embed_text(question)
    if not query_vector:
        print("问题向量化失败")
        return []

    # 2. 向量归一化（核心优化：必须和文档入库时的处理一致）
    if VECTOR_NORM:
        query_vector = normalize_vector(query_vector)
        if not query_vector:
            print("向量归一化失败")
            return []

    # 3. 构造优化后的向量检索DSL
    search_body = {
        "size": top_k,
        "query": {
            "knn": {  # ES 8.x HNSW索引（推荐）
                "field": "vector",
                "query_vector": query_vector,
                "k": top_k,
                "num_candidates": num_candidates,
                "parameters": {  # 新增：HNSW调优参数
                    "ef_search": ef_search
                }
            }
        },
        "_source": ["content", "title"],  # 只返回需要的字段
        "sort": [{"_score": {"order": "desc"}}]  # 显式按相似度降序
    }

    try:
        # 执行向量检索（添加超时和重试机制）
        response = es.search(
            index=INDEX_NAME,
            body=search_body,
            request_timeout=30  # 超时时间（避免卡死）
        )
        hits = response.get("hits", {}).get("hits", [])
        if not hits:
            print(f"未检索到相关文档（问题：{question}）")
            return []

        # 提取结果（含相似度得分，保留原始字段）
        results = []
        for hit in hits:
            source = hit.get("_source", {})
            results.append({
                "content": source.get("content", ""),
                "title": source.get("title", ""),
                "score": round(hit.get("_score", 0.0), 4),  # 保留4位小数
                "doc_id": hit.get("_id")
            })

        print(f"检索完成：问题「{question}」共匹配 {len(results)} 条结果")
        return results

    except NotFoundError:
        print(f"向量索引 {INDEX_NAME} 不存在，请先创建索引")
        return []
    except Exception as e:
        print(f"向量检索未知错误：{str(e)}")
        return []


if __name__ == "__main__":
    # 测试向量检索（对比优化前后效果）
    test_question = "实验一的实验目的是什么"
    # 优化前：使用默认参数
    res_optimized = vector_search(test_question)
    print("\n===== 优化后检索结果 =====")
    if res_optimized:
        for idx, item in enumerate(res_optimized, 1):
            print(f"{idx}. 得分：{item['score']:.4f} | 标题：{item['title']} | 内容：{item['content'][:100]}")
    else:
        print("未检索到结果")

    # 可选：测试调参效果（比如增大top_k）
    # res_more = vector_search(test_question, top_k=10)
    # print(f"\n增大top_k到10的结果数：{len(res_more)}")