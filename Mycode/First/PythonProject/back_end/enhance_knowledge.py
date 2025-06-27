import fitz  # PyMuPDF

# 提取 PDF 文本的函数
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

# 提取所有文献的文本
pdf_folder = "wenxian/"
pdf_files = [f"s{i}.pdf" for i in range(1, 11)]  # s1.pdf 到 s10.pdf
documents = {}

for pdf_file in pdf_files:
    pdf_path = f"{pdf_folder}/{pdf_file}"
    text = extract_text_from_pdf(pdf_path)
    documents[pdf_file] = text

# 打印第一篇文献的前500个字符
print(documents['s1.pdf'][:500])

def split_text(text, chunk_size=500):
    # 通过指定字符长度来分段
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 为每篇文献分段
document_segments = {}

for pdf_file, text in documents.items():
    segments = split_text(text)
    document_segments[pdf_file] = segments

# 打印第一篇文献的前几个段落
print(document_segments['s1.pdf'][:3])  # 打印前三个段落

from sentence_transformers import SentenceTransformer

# 选择一个支持中文的多语言模型
embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def get_embeddings(texts):
    # texts: list of str
    return embedder.encode(texts, show_progress_bar=True)

# 测试
sample = document_segments['s1.pdf'][:3]
vecs = get_embeddings(sample)
for i, v in enumerate(vecs):
    print(f"第{i+1}段 → 向量长度 {len(v)}")