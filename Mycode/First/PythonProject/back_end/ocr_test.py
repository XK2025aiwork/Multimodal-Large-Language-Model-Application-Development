import easyocr

# 创建 EasyOCR 阅读器，禁用 GPU
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

# 读取图片并识别文字
results = reader.readtext('hh.png')

# 输出识别结果
for result in results:
    print(result)
