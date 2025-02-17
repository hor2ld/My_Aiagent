# moonshot_ai.py
import time
import pyaudio
import requests
import json
import pyautogui
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame, StringVar
from tkinter import ttk

style = ttk.Style()
style.theme_use("clam")  # 使用更现代的主题

# 设置百度语音识别的API密钥和服务地址
api_key = "cC1ZI3NMLHWhJw65uVLVQjQH"
secret_key = "M4qJjPoU1jkUZCD6FrAhmhSfu5pq0BgA"
url = "https://vop.baidu.com/server_api"

#client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# Moonshot API的URL
MOONSHOT_API_URL = "https://api.moonshot.cn/v1/chat/completions"

# Moonshot API的密钥
MOONSHOT_API_KEY = "sk-RFzdq5yuhoPX1aTRxNibO94foJNPrcgLmxDfM3xw3A2ZIhkM"

# 初始化Moonshot客户端
client_moonshot = requests.Session()
client_moonshot.headers.update({
    "Authorization": f"Bearer {MOONSHOT_API_KEY}",
    "Content-Type": "application/json"
})

# 隐藏桌面
def hide_desktop():
    pyautogui.hotkey('win', 'd')

# 显示文本
def show_text(text):
    # 这里可以使用OpenCV或其他库来显示文本
    print(text)

# 处理用户输入并调用Moonshot生成回答
def process_user_input(user_input, root):
    if user_input.lower() in ["退出", "exit", "quit"]:
        root.quit()  # 退出程序
        return

    data = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": user_input}
        ],
        "tools": [{
            "type": "function",
            "function": {
                "name": "CodeRunner",
                "description": "代码执行器，支持运行 python 和 javascript 代码",
                "parameters": {
                    "properties": {
                        "language": {
                            "type": "string",
                            "enum": ["python", "javascript"]
                        },
                        "code": {
                            "type": "string",
                            "description": "代码写在这里"
                        }
                    },
                    "type": "object"
                }
            }
        }],
        "temperature": 0.3
    }
    response = client_moonshot.post(MOONSHOT_API_URL, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]
    else:
        return "Error: Unable to process command"

# 获取百度语音识别的访问令牌
def get_access_token(api_key, secret_key):
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    response = requests.get(token_url)
    if response.status_code == 200:
        return json.loads(response.text)["access_token"]
    else:
        raise Exception(f"Failed to get access token. Status code: {response.status_code}, Response: {response.text}")

def record_audio(duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音...")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return b''.join(frames)
# 发送语音识别请求
def recognize_speech(audio_data, access_token):
    headers = {"Content-Type": "audio/wav; rate=16000"}
    params = {"dev_pid": 1537, "token": access_token, "cuid": "your_cuid_here"}
    response = requests.post(url, headers=headers, params=params, data=audio_data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Failed to recognize speech. Status code: {response.status_code}, Response: {response.text}")
import threading

# 语音交互
def voice_interaction(text_area, stop_event, root):
    engine = pyttsx3.init()  # 初始化语音合成引擎
    voice_window = None  # 初始化 voice_window 变量
    stop_event = threading.Event()  # 创建一个事件对象用于停止线程

    def close_voice_window():
        nonlocal voice_window
        if voice_window:
            voice_window.destroy()
            voice_window = None
        stop_event.set()  # 设置事件，通知线程停止

    def voice_thread():
        while not stop_event.is_set():
            try:
                # 获取用户语音输入
                print("请说话...")
                audio_data = record_audio()

                # 获取访问令牌
                access_token = get_access_token(api_key, secret_key)

                # 调用百度云语音识别
                result = recognize_speech(audio_data, access_token)

                if result['err_no'] == 0:
                    user_input = result['result'][0]
                    print("你说的是：", user_input)

                    if user_input.lower() in ["退出", "exit", "quit"]:
                        close_voice_window()  # 关闭语音窗口
                        root.quit()  # 退出程序
                        return

                    # 处理用户输入
                    response = process_user_input(user_input)

                    # 显示回答
                    show_text(response)

                    # 更新显示区
                    text_area.insert(tk.END, f"你: {user_input}\n")
                    text_area.insert(tk.END, f"AI: {response}\n")

                    # 语音播报回答
                    engine.say(response)
                    engine.runAndWait()
                else:
                    print("语音识别失败：", result['err_msg'])

                # 添加延迟，例如每秒发送一次请求
                time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")

    # 创建并启动语音交互线程
    voice_thread = threading.Thread(target=voice_thread)
    voice_thread.start()

# 文本交互
def text_interaction():
    stop_event = threading.Event()  # 创建一个事件对象用于停止线程

    def send_message(event=None):
        try:
            user_input = entry.get()
            entry.delete(0, tk.END)
            # 处理用户输入
            response = process_user_input(user_input, root)
            # 显示回答
            show_text(response)
            # 语音播报回答
            engine.say(response)
            engine.runAndWait()
            text_area.insert(tk.END, f"你: {user_input}\n")
            text_area.insert(tk.END, f"AI: {response}\n")
        except Exception as e:
            print(f"Error: {e}")

    def toggle_voice_mode():
        nonlocal is_voice_mode
        is_voice_mode = not is_voice_mode
        if is_voice_mode:
            voice_button.config(text="切换到文本模式")
            voice_window = tk.Toplevel()  # 使用 Toplevel 创建新窗口
            voice_window.title("语音交互")
            voice_text_area = scrolledtext.ScrolledText(voice_window, wrap=tk.WORD, width=40, height=10)
            voice_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            voice_interaction(voice_text_area)  # 传递新的 text_area 对象
        else:
            voice_button.config(text="切换到语音模式")

    def on_closing():
        nonlocal is_voice_mode
        if is_voice_mode:
            stop_event.set()  # 设置事件，通知语音线程停止
        root.destroy()  # 销毁主窗口

    root = tk.Tk()  # 使用 tk.Tk() 创建主窗口
    root.title("Moonshot AI")
    root.protocol("WM_DELETE_WINDOW", on_closing)  # 绑定窗口关闭事件

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)  # 使用 tk.WORD
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    input_frame = Frame(root)
    input_frame.pack(padx=10, pady=10, fill=tk.X)

    entry = Entry(input_frame, width=30)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    entry.bind("<Return>", send_message)

    send_button = Button(input_frame, text="发送", command=send_message)
    send_button.pack(side=tk.RIGHT)

    voice_button = Button(root, text="切换到语音模式", command=toggle_voice_mode)
    voice_button.pack(padx=10, pady=10)

    engine = pyttsx3.init()  # 初始化语音合成引擎
    is_voice_mode = False

    root.mainloop()

# 主函数
def main():
    # 隐藏桌面
    # hide_desktop()

    # 文本交互
    text_interaction()

if __name__ == "__main__":
    main()
