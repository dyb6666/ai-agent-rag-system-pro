from openai import OpenAI
from config import OPENAI_API_KEY, DEEPSEEK_BASE_URL

# 初始化 OpenAI 客户端（指向 DeepSeek 服务器）
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=DEEPSEEK_BASE_URL  # 核心：对接 DeepSeek 的 OpenAI 兼容接口
)

def generate_answer(prompt):
    """
    调用 DeepSeek API 生成回答（OpenAI 风格）
    核心规则：严格基于上下文回答，不编造信息
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # DeepSeek 免费模型
            messages=[
                # 系统提示词：强制基于上下文回答（关键）
                {"role": "system", "content": """你是一个严格基于给定上下文回答问题的助手，
1. 只使用上下文里的信息回答，绝不编造任何未提及的内容；
2. 如果上下文没有相关信息，直接回答“未找到相关答案”；
3. 回答要简洁、准确，贴合问题核心。"""},
                {"role": "user", "content": prompt}  # 传入拼接好的上下文+问题
            ],
            temperature=0.1,  # 低随机性，保证回答精准
            max_tokens=1000   # 回答最大长度
        )
        # 返回纯回答内容
        return response.choices[0].message.content.strip()
    except Exception as e:
        # 异常处理，避免程序崩溃
        return f"回答生成失败：{str(e)}"

# 测试调用（可选）
if __name__ == "__main__":
    test_prompt = """
上下文：
K-means算法是无监督聚类算法，核心是通过迭代将样本划分为k个簇，每个簇的中心是该簇所有样本的均值。

问题：K-means算法的核心是什么？
    """
    answer = generate_answer(test_prompt)
    print("LLM 回答：", answer)