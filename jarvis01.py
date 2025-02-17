# -*- coding: utf-8 -*-

from transformers import pipeline
import os
import sys
from transformers import AutoModel, AutoTokenizer

# 初始化意图分类器
intent_classifier = pipeline("text-classification", model="distilbert-base-uncased", return_all_scores=True)

def get_intent(text):
    """
    使用预训练模型识别意图

    :param text: 用户输入的文本
    :return: 识别出的意图
    """
    try:
        # 使用预训练模型识别意图
        result = intent_classifier(text)
        # 假设模型输出的第一个标签是最可能的意图
        intent = result[0][0]['label']
        return intent
    except Exception as e:
        print(f"Error occurred while getting intent: {e}")
        return None

def perform_action(intent):
    """
    根据意图执行相应的操作

    :param intent: 识别出的意图
    """
    try:
        # 根据意图执行相应的操作
        if "查找文件" in intent:
            speak("请告诉我文件名，我会帮你查找。")
            file_name = input("请输入文件名: ")
            # 在这里添加查找文件的代码
        elif "播放音乐" in intent:
            speak("请告诉我音乐名称，我会帮你播放。")
            music_name = input("请输入音乐名称: ")
            # 在这里添加播放音乐的代码
        elif "退出" in intent:
            speak("再见！")
            sys.exit()  # 终止程序
        else:
            speak("对不起，我不明白你的意图。")
    except Exception as e:
        print(f"Error occurred while performing action: {e}")

def speak(text):
    """
    将文本转换为语音

    :param text: 要转换为语音的文本
    """
    try:
        # 这里可以添加语音合成的代码，例如使用pyttsx3库
        print(text)  # 暂时使用print代替语音合成
    except Exception as e:
        print(f"Error occurred while speaking: {e}")

def main():
    """
    主函数，程序的入口点
    """
    try:
        while True:
            command = input("请输入命令: ")
            if command:
                intent = get_intent(command)
                if intent:
                    perform_action(intent)
    except KeyboardInterrupt:
        print("程序已终止。")
    except Exception as e:
        print(f"Error occurred in main function: {e}")

if __name__ == "__main__":
    # 下载模型和分词器
    model = AutoModel.from_pretrained("distilbert-base-uncased")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    # 保存模型和分词器到本地
    model.save_pretrained("D:/VSCode/MyAiAgent/local_models/distilbert-base-uncased")
    tokenizer.save_pretrained("D:/VSCode/MyAiAgent/local_models/distilbert-base-uncased")

    main()
