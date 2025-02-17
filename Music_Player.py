# -*- coding: utf-8 -*-
import sys
import requests
import json
import pyaudio
import playsound
import os  # 添加这一行
import time  # 添加这一行

# Set console encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def play_audio(file_path):
    # 获取系统默认的文件系统编码
    encoding = sys.getfilesystemencoding()
    
    # 将文件路径转换为系统默认编码
    file_path = file_path.encode(encoding).decode(encoding)
    # 播放音频文件
    playsound.playsound(file_path)

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

def main():
    # 设置百度语音识别的API密钥和服务地址
    api_key = "cC1ZI3NMLHWhJw65uVLVQjQH"
    secret_key = "M4qJjPoU1jkUZCD6FrAhmhSfu5pq0BgA"
    url = "https://vop.baidu.com/server_api"

    # 获取访问令牌
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    response = requests.get(token_url)
    access_token = json.loads(response.text)["access_token"]

    # 设置请求头和参数
    headers = {"Content-Type": "audio/wav; rate=16000"}
    params = {"dev_pid": 1537, "token": access_token, "cuid": "your_cuid_here"}

    print("请说话...")
    audio_data = record_audio()

    # 发送语音识别请求
    response = requests.post(url, headers=headers, params=params, data=audio_data)
    result = json.loads(response.text)

    if "result" in result:
        print("你说的是：", result["result"][0])

        # 假设你说的是“播放音频文件”，然后说出文件名
        if "播放音频文件" in result["result"][0]:
            file_name = result["result"][0].replace("播放音频文件", "").strip()
            file_path = os.path.join('D:', 'Work', '新建文件夹', '小学英语课本听力', f'{file_name}.mp3')  # 使用 os.path.join 来处理文件路径
            play_audio(file_path)
        else:
            print("无法识别的指令")
    else:
        print("语音识别失败：", result["err_msg"])

    # 添加延迟，例如每秒发送一次请求
    time.sleep(1)

if __name__ == "__main__":
    main()
