import pyttsx3


def text_to_speech(text):
    # 初始化语音引擎
    engine = pyttsx3.init()
    # 设置要朗读的文本
    engine.say(text)
    # 运行引擎并等待朗读完成
    engine.runAndWait()


if __name__ == "__main__":
    text = "你好，这是一个文字转语音的示例。"
    text_to_speech(text)
    
    text = "过来呀！给你介绍下这个东西。"
    text_to_speech(text)
    text = "this is apple. and that is banana."
    text_to_speech(text)