import os
import subprocess
import speech_recognition as sr
import webbrowser
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, END, Listbox, Scrollbar
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor

# 语音识别模块
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        update_display("请说话...\n")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="zh-CN")  # 使用Google API（需联网）
        print(f"你说的是: {text}")
        update_display(f"你说的是: {text}\n")
        return text
    except Exception as e:
        print("语音识别失败，请重试。")
        update_display("语音识别失败，请重试。\n")
        return None

# 自然语言理解模块
def parse_command(text):
    if text is None:
        return {"intent": "unknown"}
    
    text = text.lower()
    if "打开" in text:
        if "文件" in text:
            return {"intent": "open_file", "name": extract_filename(text)}
        elif "软件" in text:
            return {"intent": "open_app", "name": extract_app_name(text)}
    elif "搜索" in text:
        return {"intent": "search_web", "query": extract_query(text)}
    elif "退出" in text:
        return {"intent": "exit"}
    else:
        return {"intent": "unknown"}

# 搜索文件
def search_file(file_name):
    file_paths = []
    for root, dirs, files in os.walk("/"):  # 从根目录开始搜索
        for file in files:
            if file_name in file:
                file_paths.append(os.path.join(root, file))
    return file_paths

# 提取应用程序名
def extract_app_name(text):
    # 简单实现：假设应用程序名是“打开软件”后的内容
    app_name = text.split("打开软件")[-1].strip()
    return app_name

# 提取搜索查询
def extract_query(text):
    # 简单实现：假设查询是“搜索”后的内容
    query = text.split("搜索")[-1].strip()
    return query

# 提取文件名并自动搜索
def extract_filename(text):
    # 简单实现：假设文件名是“打开文件”后的内容
    file_name = text.split("打开文件")[-1].strip()
    if not file_name:
        return None

    # 使用多线程搜索文件
    with ThreadPoolExecutor() as executor:
        future = executor.submit(search_file, file_name)
        file_paths = future.result()

    if not file_paths:
        return None
    elif len(file_paths) == 1:
        return file_paths[0]
    else:
        # 创建自定义文件选择窗口
        root = tk.Tk()
        root.title("选择要打开的文件")

        # 创建列表框和滚动条
        listbox = Listbox(root, width=50, height=10)
        scrollbar = Scrollbar(root, orient=tk.VERTICAL)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        # 将匹配的文件路径添加到列表框中
        for file_path in file_paths:
            listbox.insert(END, file_path)

        # 创建打开按钮
        def open_file():
            selected_file = listbox.get(listbox.curselection())
            if os.path.exists(selected_file):
                os.startfile(selected_file)  # Windows专用
                print(f"已打开文件: {selected_file}")
                update_display(f"已打开文件: {selected_file}\n")
            else:
                print(f"文件不存在: {selected_file}")
                update_display(f"文件不存在: {selected_file}\n")

        open_button = Button(root, text="打开", command=open_file)

        # 布局组件
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        open_button.pack()

        root.mainloop()

# 系统操作执行模块
def execute_command(command):
    if command is None:
        print("未识别的指令，请重试。")
        update_display("未识别的指令，请重试。\n")
        return
    
    intent = command.get("intent")
    if intent == "open_file":
        file_paths = command.get("name")
        if file_paths:
            if isinstance(file_paths, str):
                file_paths = [file_paths]
            for file_path in file_paths:
                if os.path.exists(file_path):
                    os.startfile(file_path)  # Windows专用
                    print(f"已打开文件: {file_path}")
                    update_display(f"已打开文件: {file_path}\n")
                else:
                    print(f"文件不存在: {file_path}")
                    update_display(f"文件不存在: {file_path}\n")
        else:
            print("未找到文件，请重试。")
            update_display("未找到文件，请重试。\n")
    elif intent == "open_app":
        app_name = command.get("name")
        if app_name == "记事本":
            subprocess.Popen(["notepad.exe"])  # 打开记事本
            print("已打开记事本")
            update_display("已打开记事本\n")
        elif app_name == "计算器":
            subprocess.Popen(["calc.exe"])  # 打开计算器
            print("已打开计算器")
            update_display("已打开计算器\n")
        else:
            print(f"暂不支持打开: {app_name}")
            update_display(f"暂不支持打开: {app_name}\n")
    elif intent == "search_web":
        query = command.get("query")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        print(f"正在搜索: {query}")
        update_display(f"正在搜索: {query}\n")
    elif intent == "exit":
        print("正在退出助手...")
        update_display("正在退出助手...\n")
        root.quit()
    else:
        print("未识别的指令，请重试。")
        update_display("未识别的指令，请重试。\n")

# 更新显示区域内容
def update_display(message):
    display_area.config(state=tk.NORMAL)
    display_area.insert(tk.END, message)
    display_area.config(state=tk.DISABLED)
    display_area.yview(tk.END)  # 自动滚动到底部

# 处理文本输入
def handle_text_input():
    text = text_input.get()
    if text:
        update_display(f"你输入的是: {text}\n")
        command = parse_command(text)
        execute_command(command)
        text_input.delete(0, tk.END)  # 清空输入框

# 处理语音输入
def handle_voice_input():
    text = listen()
    if text:
        command = parse_command(text)
        execute_command(command)

# 创建GUI
root = tk.Tk()
root.title("语音助手")
root.geometry("600x400")

# 显示区域
display_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
display_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 文本输入区域
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10, fill=tk.X)

text_input = Entry(input_frame, width=50)
text_input.pack(side=tk.LEFT, padx=5)

text_button = Button(input_frame, text="发送", command=handle_text_input)
text_button.pack(side=tk.LEFT, padx=5)

# 语音输入按钮
voice_button = Button(root, text="语音输入", command=handle_voice_input)
voice_button.pack(pady=10)

# 启动主循环
root.mainloop()