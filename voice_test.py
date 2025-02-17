import speech_recognition as sr

def test_voice_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="zh-CN")
            print(f"识别结果: {text}")
        except sr.UnknownValueError:
            print("无法识别语音")
        except sr.RequestError as e:
            print(f"无法连接到语音识别服务: {e}")

if __name__ == "__main__":
    test_voice_recognition()