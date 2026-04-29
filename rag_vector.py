from vector_retriever import vector_search  # 你的向量检索函数
from llm import generate_answer  # 导入新的generate_answer


def rag_vector_query(question):
    """完整RAG流程：向量检索 → 增强Prompt构造 → 调用DeepSeek生成回答"""
    # 1. 向量检索相关文档
    retrieved_docs = vector_search(question)

    # 2. 构造增强版Prompt（核心优化）
    if not retrieved_docs:
        # 无检索结果时的兜底Prompt（避免生硬回答）
        prompt = f"""
你是一个专业的知识问答助手，请回答以下问题。
注意：目前没有找到任何相关参考文档，请基于你的知识简要回答；如果完全不知道答案，请直接回复「未找到相关答案」，不要编造内容。

问题：{question}
        """
        final_answer = generate_answer(prompt)
    else:
        # 有检索结果时的增强Prompt
        # 步骤1：格式化上下文（提升LLM可读性）
        context = "\n".join([
            f"【参考文档{idx + 1}（相似度{doc['score']:.2f}）】\n{doc['content']}"
            for idx, doc in enumerate(retrieved_docs)
        ])
        # 步骤2：增强版Prompt模板（含指令约束+上下文+问题）
        prompt = f"""
# 核心指令
1. 必须严格基于提供的「参考文档」回答问题，禁止使用任何文档外的信息；
2. 回答时优先引用相似度高的文档内容，标注文档序号（如「参考文档1」）；
3. 如果文档内容不足以回答问题，直接回复「未找到相关答案」，不要编造；
4. 回答逻辑清晰、分点说明（如果适用），语言简洁，保留专业术语。

# 参考文档
{context}

# 待回答问题
{question}
        """
        # 3. 调用DeepSeek生成回答
        final_answer = generate_answer(prompt)

    # 返回完整结果（新增prompt字段，便于调试）
    return {
        "question": question,
        "retrieved_docs": retrieved_docs,
        "prompt": prompt,  # 新增：返回构造的Prompt，方便排查问题
        "answer": final_answer
    }
# 测试完整流程
if __name__ == "__main__":
    result = rag_vector_query("K-means聚类算法原理是是什么")
    print("===== 最终问答结果 =====")
    print(f"问题：{result['question']}")
    print(f"回答：{result['answer']}")