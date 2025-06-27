import requests
from IPython.display import display, Markdown


def upload_to_picgo(image_path, api_key):
    """
    将本地图片上传到PicGo图床并返回公网URL

    参数:
    image_path: 本地图片路径
    api_key: PicGo API密钥

    返回:
    公网可访问的图片URL (失败时返回None)
    """
    url = "https://www.picgo.net/api/1/upload"

    headers = {
        "X-API-Key": api_key
    }

    try:
        with open(image_path, 'rb') as f:
            files = {'source': f}
            response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            data = response.json()
            # 从响应中提取图片URL
            return data['image']['url']
        else:
            print(f"上传失败! 状态码: {response.status_code}, 错误信息: {response.text}")
            return None

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None


# 使用示例
if __name__ == "__main__":
    # 替换为你的实际API密钥
    API_KEY = "chv_S4yb7_88d2416f56d35452835e49d8b088e1cfba2a528fb25b288e0f932c9c2355fe5b5c2f4b8f14c247ae833bb8a42039306537ce25cc147883545a371b2dbd065900"
    # 替换为你的本地图片路径
    IMAGE_PATH = "asd.png"

    public_url = upload_to_picgo(IMAGE_PATH, API_KEY)

    if public_url:
        print("上传成功! 公网访问URL:")
        print(public_url)
        print(type(public_url))

        # 在Jupyter中显示Markdown格式的图片
        display(Markdown(f"![Uploaded Image]({public_url})"))
    else:
        print("图片上传失败")