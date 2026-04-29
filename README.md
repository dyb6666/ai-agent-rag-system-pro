# AI Agent RAG System Pro

## 🚀 特性
- 多 Agent 架构
- RAG（检索增强生成）
- 向量检索
- 流式输出（SSE）
- 可接入真实大模型

## 🧠 架构
Parser → Embedding → Retrieval → Generator → Orchestrator

## ▶️ 启动
```bash
pip install -r requirements.txt
uvicorn main:app --reload