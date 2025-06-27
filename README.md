## 

```
├── First/
├── Second/          
├── Third/          
├── requirements.txt       
└── README.md              
```




## 🚀 快速开始  这里最推荐Second里安装的大模型，因为First中涉及Picgo网站的url调用，该网站经常崩掉，所以可以优先尝试Second模型的部署

### 1. 克隆仓库  

```bash  
mkdir -p ~/MyProjects
git clone https://github.com/XK2025aiwork/Multimodal-Large-Language-Model-Application-Development.git ~/MyProjects/Multimodal-Large-Language-Model-Application-Development
cd ~/MyProjects/Multimodal-Large-Language-Model-Application-Development  
```


### 2. 安装依赖  

```bash  
pip install -r requirements.txt  
```

### 3. 运行应用程序  

```bash  
# 运行应用1  
cd Mycode/First/PythonProject

python GUI.py

# 运行应用2  
cd ~/MyProjects/Multimodal-Large-Language-Model-Application-Development/Mycode/Second/siliconflow-chat/backend

python app.py &

cd ~/MyProjects/Multimodal-Large-Language-Model-Application-Development/Mycode/Second/siliconflow-chat/frontend

open -a Safari index.html

# 运行应用3  
cd Mycode/Third

open -a Safari complete626A.html
```

## 🔧 环境配置  

建议使用Python 3.8+：  

```bash  
python -m venv .venv  
source .venv/bin/activate  # Linux/macOS  
.venv\Scripts\activate     # Windows  
```

