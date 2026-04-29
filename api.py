# #FastApi接口
# from fastapi import FastAPI
# from pydantic import BaseModel
# from rag import rag_query
#
# app = FastAPI()
#
#
# class QueryRequest(BaseModel):
#     question: str
#
#
# @app.post("/chat")
# def chat(req: QueryRequest):
#
#     result = rag_query(req.question)
#
#     return result
# FastApi接口（适配向量RAG）
from fastapi import FastAPI
from pydantic import BaseModel
from rag_vector import rag_vector_query

app = FastAPI(title="向量RAG问答接口")

class QueryRequest(BaseModel):
    question: str

@app.post("/chat/vector", summary="基于向量相似度的问答")
def vector_chat(req: QueryRequest):
    result = rag_vector_query(req.question)
    return result

