# moonshot_ai.py
import os
import json
import logging
import requests
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame

# 配置日志记录
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Moonshot API 的 URL 和密钥
MOONSHOT_API_URL = "https://api.moonshot.cn/v1/chat/completions"
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY", "默认密钥")  # 使用环境变量存储 API 密钥

# 初始化 Moonshot 客户端
client = requests.Session()
client.headers.update({
    "Authorization": f"Bearer {MOONSHOT_API_KEY}",
    "Content-Type": "application/json"
})

# 隐藏桌面
def hide_desktop():
    import pyautogui
    pyautogui.hotkey('win', 'd')

# 显示文本
def show_text(text):
    print(text)

# 处理用户输入并调用 Moonshot 生成回答
def process_user_input(user_input):
    try:
        data = {
            "model": "moonshot-v1-8k",
            "messages": [
                {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手..."},
                {"role": "user", "content": user_input}
            ],
            "tools": [{
                "type": "function",
                "function": {
                    "name": "CodeRunner",
                    "description": "代码执行器，支持运行 python 和 javascript 代码",
                    "parameters": {
                        "properties": {
                            "language": {"type": "string", "enum": ["python", "javascript"]},
                            "code": {"type": "string", "description": "代码写在这里"}
                        },
                        "type": "object"
                    }
                }
            }],
            "temperature": 0.3
        }
        response = client.post(MOONSHOT_API_URL, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            logging.error(f"API 错误: {response.status_code}, {response.text}")
            return "Error: Unable to process command"
    except Exception as e:
        logging.error(f"处理用户输入时发生错误: {e}")
        return "Error: Something went wrong."

# 语音交互
def voice_interaction():
    engine = pyttsx3.init()
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("请说话...")
                audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio, language=current_language)
            print(f"识别结果: {user_input}")

            # 检查是否需要退出
            if user_input.lower() in ["退出", "停止"]:
                print("语音交互已退出。")
                break

            response = process_user_input(user_input)
            show_text(response)
            engine.say(response)
            engine.runAndWait()
        except sr.UnknownValueError:
            print("无法识别语音")
        except sr.RequestError as e:
            print(f"无法连接到语音识别服务; {e}")
        except Exception as e:
            print(f"Error: {e}")

# 文本交互
def text_interaction():
    def send_message(event=None):
        try:
            user_input = entry.get()
            entry.delete(0, tk.END)

            # 检查是否需要退出
            if user_input.lower() in ["退出", "停止"]:
                root.quit()

            response = process_user_input(user_input)
            text_area.insert(tk.END, f"你: {user_input}\n")
            text_area.insert(tk.END, f"AI: {response}\n")
            engine.say(response)
            engine.runAndWait()
        except Exception as e:
            print(f"Error: {e}")

    def toggle_voice_mode():
        nonlocal is_voice_mode
        is_voice_mode = not is_voice_mode
        if is_voice_mode:
            voice_button.config(text="切换到文本模式")
            voice_interaction()
        else:
            voice_button.config(text="切换到语音模式")

    def clear_chat():
        text_area.delete(1.0, tk.END)

    def toggle_language():
        nonlocal current_language
        current_language = "en-US" if current_language == "zh-CN" else "zh-CN"
        language_button.config(text=f"当前语言: {current_language}")

    # 初始化 GUI
    root = tk.Tk()
    root.title("Moonshot AI")

    # 聊天显示区域
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # 输入框和按钮
    input_frame = Frame(root)
    input_frame.pack(padx=10, pady=10, fill=tk.X)

    entry = Entry(input_frame, width=30)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    entry.bind("<Return>", send_message)

    send_button = Button(input_frame, text="发送", command=send_message)
    send_button.pack(side=tk.RIGHT)

    # 功能按钮
    voice_button = Button(root, text="切换到语音模式", command=toggle_voice_mode)
    voice_button.pack(padx=10, pady=5)

    clear_button = Button(root, text="清空聊天记录", command=clear_chat)
    clear_button.pack(padx=10, pady=5)

    language_button = Button(root, text=f"当前语言: {current_language}", command=toggle_language)
    language_button.pack(padx=10, pady=5)

    # 初始化语音合成引擎
    engine = pyttsx3.init()
    set_voice_properties(engine, rate=150, volume=1.0, voice_id=0)

    # 状态变量
    is_voice_mode = False
    current_language = "zh-CN"

    root.mainloop()

# 设置语音合成引擎的个性化属性
def set_voice_properties(engine, rate=150, volume=1.0, voice_id=0):
    engine.setProperty('rate', rate)  # 设置语速
    engine.setProperty('volume', volume)  # 设置音量
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)  # 设置声音类型

# 主函数
def main():
    hide_desktop()
    text_interaction()

if __name__ == "__main__":
    main()