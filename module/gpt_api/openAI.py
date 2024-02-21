import openai

import config
# from config import prompts_path, openai_api_key, openai_api_url, cosplay_role



# 初始对话
messages = []
def init_chat():
    """
    初始化对话
    :return:
    """
    config_openai = config.Config()

    openai.api_key = config_openai.openai_api_key
    openai.api_base = config_openai.openai_api_url
    global messages
    # 从文本文件中读取提示词
    with open(config_openai.prompts_path, "r", encoding="utf-8") as file:
        prompts = file.read().splitlines()

    # 添加提示词部分
    for prompt in prompts:
        # print(prompt)
        messages.append({"role": "user", "content": prompt})

    messages += [
        {"role": "assistant", "content": "好的！让我们开始{}扮演吧！请问有什么问题或者需要我帮助的吗？".format(config_openai.cosplay_role)}
    ]




def chatgpt(user_input):
    """
    调用OpenAI聊天模型
    :param user_input: 用户输入
    :return: 模型回复
    """
    # 添加用户输入到对话中
    messages.append({"role": "user", "content": user_input})

    # 调用OpenAI聊天模型
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # 获取模型的回复消息
    model_reply = completion.choices[0].message

    # 添加模型回复到对话中
    messages.append(model_reply)

    # 输出模型回复
    print("Assistant:", model_reply["content"])
    return model_reply["content"]

# 结束对话
def end_chat():
    """
    结束对话
    :return:
    """
    print("对话结束。")
    messages.clear()


def load_chat_history():
    """
    加载历史对话消息
    :return:
    """
    # 从历史记录文件或数据库中加载历史对话消息
    # 假设历史消息以字典列表的形式存储，每个字典包含 "role" 和 "content" 属性
    # 例如：{"role": "user", "content": "Hello!"}
    history_messages = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi, how can I help you?"}
    ]

    # 将历史消息添加到当前对话中
    messages.extend(history_messages)


if __name__ == '__main__':
    init_chat()
    while True:
        user_input = input("User:")
        if user_input == "exit":
            end_chat()
            break
        chatgpt(user_input)
