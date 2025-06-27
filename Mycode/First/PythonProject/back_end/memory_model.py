class Memory:
    def __init__(self):
        # 初始化对话历史和用户画像
        self.history = []  # 存储对话历史
        self.user_profile = {}  # 存储用户画像

    def add_to_history(self, user_message, model_response):
        """
        每次用户输入和模型响应时，记录对话历史。
        """
        self.history.append({"user": user_message, "model": model_response})

    def update_user_profile(self, key, value):
        """
        更新用户画像中的信息，例如用户兴趣、常见问题等。
        """
        self.user_profile[key] = value

    def get_history(self):
        """
        获取对话历史，返回一个合并的历史字符串。
        """
        return "\n".join([f"用户: {entry['user']}\n模型: {entry['model']}" for entry in self.history])

    def get_user_profile(self):
        """
        获取用户画像信息，返回字典格式。
        """
        return self.user_profile