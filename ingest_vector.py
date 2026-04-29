# 批量文档向量化 + 插入ES
from datetime import datetime
from embedding import embed_text
from es_client import es, create_vector_index
from doc_loader import load_document
from config import INDEX_NAME


def ingest_doc_to_vector(file_path):
    """
    加载文档 → 向量化 → 插入ES向量索引
    """
    # 1. 创建向量索引（确保索引存在）
    create_vector_index(INDEX_NAME)

    # 2. 加载文档
    doc_data = load_document(file_path)
    if not doc_data:
        print("文档无有效内容")
        return

    # 3. 批量向量化 + 插入
    success_count = 0
    for item in doc_data:
        content = item["content"]
        title = item["title"]

        # 生成向量
        vector = embed_text(content)
        if not vector:
            print(f"内容向量化失败：{content[:20]}...")
            continue

        # 构造文档（含向量）
        doc = {
            "content": content,
            "title": title,
            "create_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "vector": vector
        }

        # 插入ES
        try:
            es.index(
                index=INDEX_NAME,
                body=doc,
                refresh=True  # 立即刷新索引（测试用，生产建议关闭）
            )
            success_count += 1
            print(f"插入成功：{title} - {content[:20]}...")
        except Exception as e:
            print(f"插入失败：{str(e)}")

    print(f"\n批量入库完成：成功 {success_count}/{len(doc_data)} 条")


if __name__ == "__main__":
    ingest_doc_to_vector("E:\大三\数据挖掘实践\数据挖掘应用实践-实验指导书.docx")
