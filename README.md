## 

```
├── First/
├── Second/          
├── Third/          
├── requirements.txt       
└── README.md              
```




## 🚀 快速开始  这里最推荐Second和Third里安装的大模型（也就是应用2和应用3的代码），因为First中涉及Picgo网站的url调用，该网站经常崩掉。另外，本代码使用的是macos操作系统。

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

#### 3.1应用1

```bash  
# 运行应用1  
cd ~/MyProjects/Multimodal-Large-Language-Model-Application-Development/Mycode/First/PythonProject

python GUI.py

```
#### 3.2应用2(Second 推荐)
```bash  
# 运行应用2  
cd ~/MyProjects/Multimodal-Large-Language-Model-Application-Development/Mycode/Second/siliconflow-chat/backend

python app.py

#重新再打开一个终端界面！！！！

cd ~/MyProjects/Multimodal-Large-Language-Model-Application-Development/Mycode/Second/siliconflow-chat/frontend

open -a Safari index.html
```
#### 3.3应用3(Third 推荐)
```bash  
cd ~/MyProjects/Multimodal-Large-Language-Model-Application-Development/Mycode/Third

open -a Safari complete626A.html
```

## 🔧 环境配置  

建议使用Python 3.8+：  

```bash  
python -m venv .venv  
source .venv/bin/activate  # Linux/macOS  
.venv\Scripts\activate     # Windows  
```

