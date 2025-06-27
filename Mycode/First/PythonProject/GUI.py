import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
from datetime import datetime
import os
import sys
sys.path.append("./back_end")
from Main import Main_picture,Main_text

def get_screenshot_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"screenshot_{timestamp}.png"

# 初始化截图操作
# def take_screenshot():
#     output_text.place_forget()
#     screenshot_button.place_forget()
#     show_code_button.place_forget()
#     dropdown_menu.place_forget()
#     temperature_label.place_forget()
#     input_text.place_forget()

#     # 设置窗口为全屏并置顶，带透明度
#     root.attributes("-fullscreen", True)
#     root.attributes("-alpha", 0.3)
#     # 替换为：
#     # root.attributes("-topmost", True)
#     # root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
#     # canvas.lift()
#     root.attributes("-topmost", True)

#     # 显示画布并开始监听鼠标事件
#     canvas.pack(fill=tk.BOTH, expand=True)
#     canvas.delete("all")  # 清除历史痕迹
#     canvas.configure(cursor="crosshair")
#     canvas.bind("<ButtonPress-1>", on_click)
#     canvas.bind("<B1-Motion>", on_drag)
#     canvas.bind("<ButtonRelease-1>", on_release)

#     messagebox.showinfo("提示", "请拖动鼠标选择截图区域")
# def take_screenshot():
#     output_text.place_forget()
#     screenshot_button.place_forget()
#     show_code_button.place_forget()
#     dropdown_menu.place_forget()
#     temperature_label.place_forget()
#     input_text.place_forget()
#     text_input.place_forget()
#     text_input_label.place_forget()

#     # 让 canvas 占据整个屏幕大小，但不是全屏窗口
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     root.geometry(f"{screen_width}x{screen_height}+0+0")
#     root.attributes("-topmost", True)

#     canvas.place(x=0, y=0, width=screen_width, height=screen_height)
#     canvas.lift()
#     canvas.delete("all")
#     canvas.configure(cursor="crosshair")
#     canvas.bind("<ButtonPress-1>", on_click)
#     canvas.bind("<B1-Motion>", on_drag)
#     canvas.bind("<ButtonRelease-1>", on_release)

#     messagebox.showinfo("提示", "请拖动鼠标选择截图区域")
# def take_screenshot():
#     # 创建一个新的顶层窗口
#     screenshot_window = tk.Toplevel(root)
#     screenshot_window.attributes("-fullscreen", True)
#     screenshot_window.attributes("-alpha", 0.3)  # 半透明
#     screenshot_window.attributes("-topmost", True)
#     screenshot_window.configure(bg='gray')
    
#     canvas = tk.Canvas(screenshot_window, cursor="crosshair", bg='gray')
#     canvas.pack(fill=tk.BOTH, expand=True)

#     messagebox.showinfo("提示", "请拖动鼠标选择截图区域")

#     # 在 enclosing scope 定义变量
#     start_x = start_y = rect = None

#     def on_click(event):
#         nonlocal start_x, start_y, rect
#         start_x = event.x
#         start_y = event.y
#         rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

#     def on_drag(event):
#         nonlocal rect, start_x, start_y
#         canvas.coords(rect, start_x, start_y, event.x, event.y)

#     def on_release(event):
#         nonlocal start_x, start_y, rect
#         end_x, end_y = event.x, event.y
#         x1, y1 = screenshot_window.winfo_rootx() + min(start_x, end_x), screenshot_window.winfo_rooty() + min(start_y, end_y)
#         x2, y2 = screenshot_window.winfo_rootx() + max(start_x, end_x), screenshot_window.winfo_rooty() + max(start_y, end_y)

#         screenshot_window.withdraw()  # 先隐藏窗口防止截图时把它拍进去

#         try:
#             screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
#             filename = get_screenshot_filename()
#             if not os.path.exists("screenshots"):
#                 os.makedirs("screenshots")
#             save_path = os.path.join("screenshots", filename)
#             screenshot.save(save_path)
#             messagebox.showinfo("截图完成", f"截图已保存到：{save_path}")
#         except Exception as e:
#             messagebox.showerror("错误", f"截图失败：{e}")
#         finally:
#             screenshot_window.destroy()  # 完全销毁截图窗口

#     canvas.bind("<ButtonPress-1>", on_click)
#     canvas.bind("<B1-Motion>", on_drag)
#     canvas.bind("<ButtonRelease-1>", on_release)

import subprocess
import tempfile

def take_screenshot():
    messagebox.showinfo("提示", "请用鼠标框选截图区域，按 Enter 完成，Esc 取消。")

    filename = get_screenshot_filename()
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    save_path = os.path.join("screenshots", filename)

    try:
        # 使用系统截图工具（macOS 原生）
        result = subprocess.run(["screencapture", "-i", save_path], check=True)

        if os.path.exists(save_path):
            messagebox.showinfo("截图完成", f"截图已保存到：{save_path}")
        else:
            messagebox.showwarning("取消", "截图已被取消。")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"截图失败：{e}")


# # 鼠标按下
# def on_click(event):
#     global start_x, start_y, rect
#     start_x = event.x
#     start_y = event.y
#     rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=3)

# # 鼠标拖动
# def on_drag(event):
#     end_x = event.x
#     end_y = event.y
#     canvas.coords(rect, start_x, start_y, end_x, end_y)

# # 鼠标释放完成截图
# def on_release(event):
#     end_x = event.x
#     end_y = event.y
#     x1, y1 = min(start_x, end_x), min(start_y, end_y)
#     x2, y2 = max(start_x, end_x), max(start_y, end_y)

#     # 执行截图
#     screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
#     filename = get_screenshot_filename()
#     if not os.path.exists("screenshots"):
#         os.makedirs("screenshots")
#     save_path = os.path.join("screenshots", filename)
#     screenshot.save(save_path)
#     messagebox.showinfo("截图完成", f"截图已保存到：{save_path}")

#     # 清除画布内容和解绑事件
#     canvas.delete("all")
#     canvas.unbind("<ButtonPress-1>")
#     canvas.unbind("<B1-Motion>")
#     canvas.unbind("<ButtonRelease-1>")
#     canvas.pack_forget()

#     # 恢复窗口设置
#     root.attributes("-fullscreen", False)
#     root.attributes("-alpha", 1.0)
#     root.attributes("-topmost", False)

#     # 恢复 UI
#     output_text.place(x=50, y=170, width=500, height=240)
#     screenshot_button.place(x=200, y=130)
#     show_code_button.place(x=300, y=130)
#     dropdown_menu.place(x=200, y=20)
#     temperature_label.place(x=200, y=70)
#     input_text.place(x=290, y=70, width=100, height=30)  # 高度调整为适合单行输入

def get_latest_file(folder_path):
    # 获取文件夹中所有文件的完整路径列表
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
             os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        return "文件夹中没有文件。"

    # 按照修改时间排序，取最新的那个
    latest_file = max(files, key=os.path.getmtime)
    return os.path.basename(latest_file)

def stream_output(text, index=0):
    if index == 0:
        output_text.delete('1.0', tk.END)  # 每次流式输出前清空旧内容

    if text and index < len(text):
        output_text.insert(tk.END, text[index])
        output_text.see(tk.END)
        root.after(20, stream_output, text, index + 1)


def show_function_code():
    selected_option = dropdown_var.get()
    user_input = input_text.get().strip()  # 改为使用get()获取单行输入内容
    # 首先清空输出框并立即显示提示信息
    Text_input = text_input.get().strip()
    if Text_input != '':
        output_text.delete('1.0', tk.END)  # 清空输出框
        output_text.insert(tk.END, "文献解析中，请稍后……")  # 直接插入提示文本
        output_text.see(tk.END)  # 确保提示信息可见
        root.update_idletasks()  # 强制立即更新UI，使提示立即可见
        code = Main_text(selected_option, float(user_input), Text_input)
        stream_output(code)
        return
    output_text.delete('1.0', tk.END)  # 清空输出框
    output_text.insert(tk.END, "文献解析中，请稍后……")  # 直接插入提示文本
    output_text.see(tk.END)  # 确保提示信息可见
    root.update_idletasks()  # 强制立即更新UI，使提示立即可见




    # 检查输入内容是否为空或无效
    if not user_input:
        stream_output("⚠️ 请提供有效的输入。\n")
        return

    try:
        temp = float(user_input)
    except ValueError:
        stream_output("⚠️ 输入无效，请输入数字。\n")
        return

    try:
        latest_file = get_latest_file('screenshots')
        if not latest_file:
            stream_output("⚠️ 未找到截图文件。\n")
            return

        code = Main_picture(selected_option, temp, 'screenshots/' + latest_file)
        if not code:
            stream_output("⚠️ 数据校验失败，有敏感词或注入，请重新上传。\n")
            return

        stream_output(code)
    except Exception as e:
        stream_output(f"❌ 出错了：{e}\n")


# 创建窗口
root = tk.Tk()
root.title("文献阅读助手")
root.geometry("600x500")

# 创建画布
canvas = tk.Canvas(root, bg='gray')
canvas.pack_forget()

# 下拉框选项
options = [
    "Qwen/Qwen2-VL-72B-Instruct",
    "Qwen/QVQ-72B-Preview",
    "deepseek-ai/deepseek-vl2"
]
dropdown_var = tk.StringVar()
dropdown_var.set(options[0])  # 默认选项

# 使用place布局控件
dropdown_menu = tk.OptionMenu(root, dropdown_var, *options)
dropdown_menu.place(x=200, y=20)

# 添加"temperature:"标签
temperature_label = tk.Label(root, text="temperature:")
temperature_label.place(x=200, y=65)

# 单行输入框（带缺省值0.8），内容居中显示
input_text = tk.Entry(root, justify='center')  # 使用Entry控件并设置内容居中
input_text.place(x=290, y=65, width=100, height=30)  # 调整高度为30
input_text.insert(0, "0.8")  # 设置缺省值

text_input_label = tk.Label(root, text="文献:")
text_input_label.place(x=50, y=425)
text_input = tk.Entry(root, justify='center')  # 使用Entry控件并设置内容居中
text_input.place(x=90, y=425, width=460, height=30)  # 调整高度为30


# 显示代码按钮
show_code_button = tk.Button(root, text="文献分析", command=show_function_code)
show_code_button.place(x=313, y=120)

# 截图按钮
screenshot_button = tk.Button(root, text="文献摘取", command=take_screenshot)
screenshot_button.place(x=213, y=120)

# 输出文本框
output_text = tk.Text(root, height=20, width=60)
output_text.place(x=50, y=170, width=500, height=240)

# 启动主循环
root.mainloop()