# 文档加载工具：支持txt、docx、pdf（需安装依赖）
import os
from docx import Document  # 处理docx: pip install python-docx

def load_txt(file_path):
    """加载txt文档"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return [{"content": content, "title": os.path.basename(file_path)}]

def load_docx(file_path):
    """加载docx文档"""
    doc = Document(file_path)
    contents = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            contents.append({
                "content": text,
                "title": os.path.basename(file_path)
            })
    return contents



def load_document(file_path):
    """统一文档加载入口"""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    else:
        raise ValueError(f"不支持的文件格式：{ext}")

if __name__ == "__main__":
    # 测试加载
    test_doc = "E:\大三\数据挖掘实践\数据挖掘应用实践-实验指导书.docx"
    data = load_document(test_doc)
    print(f"加载到 {len(data)} 条数据")
    print(data[0])