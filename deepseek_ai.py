import os
import sys
import time
import pyttsx3
import pyaudio
import cv2
import pyautogui
import tkinter as tk
from tkinter import scrolledtext, Entry, Button
from deepseek import DeepSeekClient  # 导入DeepSeek SDK

# 初始化语音引擎
engine = pyttsx3.init()

# DeepSeek API的URL
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"

# DeepSeek API的密钥
DEEPSEEK_API_KEY = "sk-fd003e2db5f7418e84ec2207a9f6ff54"

# 初始化DeepSeek客户端
client = DeepSeekClient(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)

# 隐藏桌面
def hide_desktop():
    pyautogui.hotkey('win', 'd')

# 显示文本
def show_text(text):
    # 这里可以使用OpenCV或其他库来显示文本
    print(text)

# 显示图片或图表
def show_image(image_path):
    # 这里可以使用OpenCV或其他库来显示图片或图表
    image = cv2.imread(image_path)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 语音交互
def voice_interaction():
    while True:
        # 获取用户语音输入
        user_input = input("请输入你的问题: ")

        # 处理用户输入
        response = process_user_input(user_input)

        # 显示回答
        show_text(response)

        # 语音播报回答
        engine.say(response)
        engine.runAndWait()

# 文本交互
def text_interaction():
    def send_message():
        user_input = entry.get()
        entry.delete(0, tk.END)
        # 处理用户输入
        response = process_user_input(user_input)
        # 显示回答
        show_text(response)
        # 语音播报回答
        engine.say(response)
        engine.runAndWait()
        text_area.insert(tk.END, f"你: {user_input}\n")
        text_area.insert(tk.END, f"AI: {response}\n")

    root = tk.Tk()
    root.title("DeepSeek AI")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
    text_area.pack(padx=10, pady=10)

    entry = Entry(root, width=30)
    entry.pack(padx=10, pady=10)

    send_button = Button(root, text="发送", command=send_message)
    send_button.pack(padx=10, pady=10)

    root.mainloop()

# 处理用户输入并调用DeepSeek生成回答
def process_user_input(user_input):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )
    return response.choices[0].message.content

# 显示桌面
def show_desktop():
    pyautogui.hotkey('win', 'd')

# 开机自启动
def auto_start():
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)

    # 创建快捷方式
    shortcut_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'deepseek_ai.lnk')
    with open(shortcut_path, 'w') as f:
        f.write(f'[InternetShortcut]\nURL=file:///{script_path}')

# 主函数
def main():
    # 隐藏桌面
    hide_desktop()

    # 开机自启动
    auto_start()

    # 语音交互
    voice_interaction()

    # 文本交互
    text_interaction()

if __name__ == "__main__":
    main()
