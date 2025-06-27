

from openai import OpenAI
import argparse
import os
import json
import re
import requests
from PIL import Image
import pytesseract
from jsonschema import validate, ValidationError
from memory_model import Memory
from upload_to_image import upload_to_picgo
import tempfile
import easyocr

# —— OCR & 预处理 配置 —— #
# Windows 用户如有需要，可显式指定 tesseract 可执行文件路径：
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 敏感词列表
SENSITIVE_WORDS = [
    "暴力", "色情", "恐怖主义", "毒品", "赌博", "诈骗", "血腥",
    "自杀", "宗教极端", "邪教", "人身攻击", "种族歧视", "仇恨", "辱骂",
    "未成年人", "个人隐私", "医疗诊断", "法律建议", "金融诈骗"
]

# 注入攻击模式（正则）
INJECTION_PATTERNS = [
    r"SELECT\s+\w+\s+FROM",  # 基本模式
    r"SEL\s*ECT",  # 绕过关键词检测
    r"UNION\s+SELECT",  # UNION注入
    r"1\s+OR\s+1\s*=\s*1",  # 永真条件
    r"';?\s*DROP\s+TABLE",  # 删除表结构
]

def extract_text_from_image(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"图片文件不存在: {path}")
    
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang='chi_sim')
    if not text.strip():
        raise RuntimeError("OCR 未识别到任何文本")
    return text

def contains_sensitive_words(text: str) -> bool:
    text_lower = text.lower()
    return any(word.lower() in text_lower for word in SENSITIVE_WORDS)

def contains_injection_patterns(text: str) -> bool:
    return any(re.search(p, text) for p in INJECTION_PATTERNS)

def process_image_url(url: str) -> str:
    # 下载图片
    resp = requests.get(url, stream=True)
    if resp.status_code != 200:
        raise RuntimeError(f"图片下载失败，HTTP {resp.status_code}")

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
        tmp_path = tmp_file.name
        for chunk in resp.iter_content(1024):
            tmp_file.write(chunk)
    
    try:
        # OCR 提取文本
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        results = reader.readtext(tmp_path)
        
        result = ''
        for i in results:
            result += i[1] + ' '
        text = result.strip()

        # 预处理校验
        if contains_sensitive_words(text):
            raise RuntimeError("提取文本中包含敏感词，请修改后再试。")
        if contains_injection_patterns(text):
            raise RuntimeError("提取文本中含有潜在的指令注入，请修改后再试。")
        
        return text
    finally:
        # 确保临时文件被删除
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

# —— JSON Schema 定义 —— #
input_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "image_url": {"type": "string", "format": "uri"},
        "tasks": {"type": "array",
                  "items": {"type": "string", "enum": ["translate", "summarize", "define_terms", "recommend"]},
                  "minItems": 1},
        "base_prompt": {"type": "string"},
        "model": {"type": "object", "properties": {"provider": {"type": "string", "enum": ["openai", "qwen"]},
                                                   "model_name": {"type": "string"},
                                                   "temperature": {"type": "number", "minimum": 0, "maximum": 2}},
                  "required": ["provider", "model_name", "temperature"]}
    },
    "required": ["image_url", "tasks", "model"]
}

output_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"results": {"type": "object",
                               "properties": {"translate": {"type": "string"}, "summarize": {"type": "string"},
                                              "define_terms": {"type": "object",
                                                               "additionalProperties": {"type": "string"}},
                                              "recommend": {"type": "array", "items": {"type": "object", "properties": {
                                                  "title": {"type": "string"}, "author": {"type": "string"},
                                                  "summary": {"type": "string"}, "research_unit": {"type": "string"},
                                                  "conclusion": {"type": "string"}}, "required": ["title", "author",
                                                                                                  "summary",
                                                                                                  "research_unit",
                                                                                                  "conclusion"]}}},
                               "required": ["translate", "summarize", "define_terms", "recommend"]}},
    "required": ["results"]
}

def validate_json(data, schema, which="输入") -> bool:
    try:
        validate(instance=data, schema=schema)
        print(f"✅ {which} 数据符合规范！")
        return True
    except ValidationError as e:
        print(f"❌ {which} 数据校验失败: {e.message}")
        return False

# —— 配置 —— #
API_KEY = os.getenv("QWEN_API_KEY", "sk-tjbexvoonvfcimzocsuwjzskakgykpmkrzfxqbejktxfcwel")
BASE_URL = "https://api.siliconflow.cn/v1"
MODELS = [
    "Qwen/QVQ-72B-Preview",
    "deepseek-ai/deepseek-vl2",
    "Qwen/Qwen2-VL-72B-Instruct"
]

def parse_args(temp=0.8):
    parser = argparse.ArgumentParser(description="调用 Qwen/VL 模型，处理图片 + 文本，并输出结果")
    parser.add_argument("--temperature", "-t", type=float, default=temp,
                        help="模型的 temperature 参数（0~2）。")
    return parser.parse_known_args()[0]

# 在主函数或者初始化的地方，先创建 Memory 实例
memory = Memory()

def Main_text(model, temp, text):
    from io import StringIO
    output_buffer = StringIO()
    output_buffer.write('✅ 数据符合规范！\n')

    # 外部 OCR 仅作安全/校对
    try:
        output_buffer.write("✅ 外部 OCR 预处理成功。\n")
        print("✅ 外部 OCR 预处理成功。")
    except Exception as e:
        error_msg = f"[ERROR] 预处理失败：{str(e)}"
        output_buffer.write(error_msg + "\n")
        print(error_msg)
        return output_buffer.getvalue()

    # 初始化客户端
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    output_buffer.write(f'—— 使用 temperature = {temp} 运行 ——\n')
    print(f"\n—— 使用 temperature = {temp} 运行 ——\n")
    
    try:
        # 让模型自己 OCR，再结合外部结果做校对
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content":
                    text + '\n' + "请对上述论文中的文字进行科学严谨的翻译(公式和数学符号用latex格式表示)；"
                    + "生成该文段的科学详细的概述；对文段中出现的专业术语进行详细释义解释；"
                    + "并推荐并详细介绍3个同领域或相近领域的最新研究成果，具体到研究单位和结论。"
                }
            ],
            stream=True,
            temperature=temp
        )
        
        # 逐字输出
        for chunk in resp:
            delta = chunk.choices[0].delta.content or ""
            output_buffer.write(delta)
            # print(delta, end="", flush=True)

    except Exception as e:
        error_msg = f"[ERROR] 调用失败：{e}"
        output_buffer.write(error_msg + "\n")
        print(error_msg)
    
    return output_buffer.getvalue()

def Main_picture(model, temp, path="test_image.jpg"):
    from io import StringIO
    output_buffer = StringIO()
    output_buffer.write('✅ 数据符合规范！\n')
    
    key = "chv_S4yb7_88d2416f56d35452835e49d8b088e1cfba2a528fb25b288e0f932c9c2355fe5b5c2f4b8f14c247ae833bb8a42039306537ce25cc147883545a371b2dbd065900"
    url = upload_to_picgo(path, key)
    args = parse_args(temp)

    # 构造输入并校验
    input_data = {
        "image_url": url,
        "tasks": ["translate", "summarize", "define_terms", "recommend"],
        "base_prompt": (
            "请对上述论文截图中的文字进行科学严谨的翻译(公式和数学符号用latex格式表示)；"
            "生成该文段的科学详细的概述；对文段中出现的专业术语进行详细释义解释；"
            "并推荐并详细介绍3个同领域或相近领域的最新研究成果，具体到研究单位和结论。"
        ),
        "model": {"provider": "qwen", "model_name": model, "temperature": args.temperature}
    }

    if not validate_json(input_data, input_schema, which="输入"):
        output_buffer.write("❌ 输入数据校验失败\n")
        return output_buffer.getvalue()

    # 外部 OCR 仅作安全/校对
    try:
        extracted = process_image_url(input_data["image_url"])
        output_buffer.write("✅ 外部 OCR 预处理成功。\n")
        print("✅ 外部 OCR 预处理成功。")
    except Exception as e:
        error_msg = f"[ERROR] 预处理失败：{str(e)}"
        output_buffer.write(error_msg + "\n")
        print(error_msg)
        return output_buffer.getvalue()

    full_prompt = f"{input_data['base_prompt']}\n\n相关文献片段:\n"

    # 初始化客户端
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    output_buffer.write(f'—— 使用 temperature = {args.temperature} 运行 ——\n')
    print(f"\n—— 使用 temperature = {args.temperature} 运行 ——\n")
    
    try:
        # 让模型自己 OCR，再结合外部结果做校对
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": input_data["image_url"]}},
                    {"type": "text", "text": f"（辅助 OCR 结果，已预处理）:\n{extracted}"},
                    {"type": "text", "text": full_prompt}
                ]}
            ],
            stream=True,
            temperature=args.temperature
        )
        
        # 逐字输出
        for chunk in resp:
            delta = chunk.choices[0].delta.content or ""
            output_buffer.write(delta)
            # print(delta, end="", flush=True)

        # 记录对话历史
        user_message = input_data["base_prompt"]  # 用户的请求
        model_response = output_buffer.getvalue()  # 模型的响应
        memory.add_to_history(user_message, model_response)  # 更新对话历史

        # 更新用户画像
        if "领域" in user_message:
            memory.update_user_profile("兴趣", "某个领域")

    except Exception as e:
        error_msg = f"[ERROR] 调用失败：{e}"
        output_buffer.write(error_msg + "\n")
        print(error_msg)
    
    return output_buffer.getvalue()

if __name__ == "__main__":
    print(Main_picture("Qwen/Qwen2-VL-72B-Instruct", 0.8, 'test_image.jpg'))
