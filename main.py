import os
from dotenv import load_dotenv  # ← 新增
load_dotenv()  # ← 新增：自动加载 .env 文件
from flask import Flask, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import dashscope
from dashscope import Generation

# 初始化 Flask
app = Flask(__name__)
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
# dashscope.api_key ='sk-ef9da958302f488b946da484bb824de3'

# === 预加载 PDF（放在项目根目录）===
loader = PyPDFLoader("manual.pdf")  # ← 你自己的 PDF
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# === 创建向量库 ===
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(splits, embeddings)
retriever = vectorstore.as_retriever()

# === Qwen 调用 ===
def qwen_generate(prompt: str) -> str:
    response = Generation.call(model="qwen-max", prompt=prompt)
    return response.output.text

# === API 接口 ===
@app.route("/query", methods=["POST"])
def query():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "Question is required"}), 400

    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    
    try:
        answer = qwen_generate(prompt)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))