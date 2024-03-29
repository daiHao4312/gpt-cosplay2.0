import json

class Config:
    def __init__(self):
        self.prompts_path = ""
        self.openai_api_key = ""
        self.openai_api_url = ""
        self.cosplay_role = ""

        self.vits_api_url = ""
        self.vits_wav_path = ""
        self.vits_id = ""
        self.vits_lang = ""
        self.vits_length = ""

        self.voice_wav_path = ""
        self.input_mode = ""
        self.database_path = ""

        self.vits_model = ""
        self.gpt_model = ""
        self.openai_chat_mode = ""

        self.gptSoVits_id = ""
        self.gptSoVits_lang = ""
        self.gptSoVits_preset = ""
        self.gptSoVits_prompt_lang = ""
        self.gptSoVits_api_url = ""
        self.gptSoVits_wav_path = ""

        self.read_config()


    def read_config(self):
        """读取配置"""
        with open("config.json") as json_file:
            config = json.load(json_file)

        openai_config = config.get("openai_config", {})
        vits_config = config.get("vits_config", {})
        gptSoVits_config = config.get("gptSoVits_config", {})

        self.gpt_model = config.get("gpt_model", "")
        self.prompts_path = openai_config.get("prompts_path", "")
        self.openai_api_key = openai_config.get("openai_api_key", "")
        self.openai_api_url = openai_config.get("openai_api_url", "")
        self.cosplay_role = openai_config.get("cosplay_role", "")
        self.openai_chat_mode = openai_config.get("openai_chat_mode", "")

        self.vits_model = config.get("vits_model", "")
        self.vits_api_url = vits_config.get("vits_api_url", "")
        self.vits_wav_path = vits_config.get("vits_wav_path", "")
        self.vits_id = vits_config.get("vits_id", "")
        self.vits_lang = vits_config.get("vits_lang", "")
        self.vits_length = vits_config.get("vits_length", "")

        self.gptSoVits_id = gptSoVits_config.get("gptSoVits_id", "")
        self.gptSoVits_lang = gptSoVits_config.get("gptSoVits_lang", "")
        self.gptSoVits_preset = gptSoVits_config.get("gptSoVits_preset", "")
        self.gptSoVits_prompt_lang = gptSoVits_config.get("gptSoVits_prompt_lang", "")
        self.gptSoVits_api_url = gptSoVits_config.get("gptSoVits_api_url", "")
        self.gptSoVits_wav_path = gptSoVits_config.get("gptSoVits_wav_path", "")

        self.voice_wav_path = config.get("voice_wav_path", "")
        self.input_mode = config.get("input_mode", "")

        self.database_path = config.get("database_path", "")

def set_vits_config_change(vits_id_input, vits_lang_input, vits_length_input, vits_api_input, vits_wav_path_input):
    """
    修改vits配置
    :param vits_id_input: vits的id
    :param vits_lang_input: vits的语言
    :param vits_length_input: vits的速度
    :param vits_api_input: vits的api地址
    :param vits_wav_path_input: vits的wav路径
    :return:
    """
    config = Config()

    config.vits_id = vits_id_input
    config.vits_lang = vits_lang_input
    config.vits_length = vits_length_input
    config.vits_api_url = vits_api_input
    config.vits_wav_path = vits_wav_path_input

    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
        config_data["vits_config"]["vits_api_url"] = config.vits_api_url
        config_data["vits_config"]["vits_wav_path"] = config.vits_wav_path
        config_data["vits_config"]["vits_id"] = config.vits_id
        config_data["vits_config"]["vits_lang"] = config.vits_lang
        config_data["vits_config"]["vits_length"] = config.vits_length

    with open("config.json", "w") as json_file:
        json.dump(config_data, json_file, indent=4)

    return config


def set_gptSoVits_config_change(gptSoVits_id_input, gptSoVits_lang_input, gptSoVits_preset_input, gptSoVits_prompt_lang_input, gptSoVits_api_input, gptSoVits_wav_path_input):
    """
    修改gptSoVits配置
    :param gptSoVits_id_input: GPTSoVits的id
    :param gptSoVits_lang_input: GPTSoVits的文本语言
    :param gptSoVits_preset_input: GPTSoVits的预设音频
    :param gptSoVits_prompt_lang_input: GPTSoVits的语言类型
    :param gptSoVits_api_input: GPTSoVits的api地址
    :param gptSoVits_wav_path_input: GPTSoVits的wav路径
    :return:
    """
    config = Config()

    config.gptSoVits_id = gptSoVits_id_input
    config.gptSoVits_lang = gptSoVits_lang_input
    config.gptSoVits_preset = gptSoVits_preset_input
    config.gptSoVits_prompt_lang = gptSoVits_prompt_lang_input
    config.gptSoVits_api_url = gptSoVits_api_input
    config.gptSoVits_wav_path = gptSoVits_wav_path_input

    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
        config_data["gptSoVits_config"]["gptSoVits_id"] = config.gptSoVits_id
        config_data["gptSoVits_config"]["gptSoVits_lang"] = config.gptSoVits_lang
        config_data["gptSoVits_config"]["gptSoVits_preset"] = config.gptSoVits_preset
        config_data["gptSoVits_config"]["gptSoVits_prompt_lang"] = config.gptSoVits_prompt_lang
        config_data["gptSoVits_config"]["gptSoVits_api_url"] = config.gptSoVits_api_url
        config_data["gptSoVits_config"]["gptSoVits_wav_path"] = config.gptSoVits_wav_path

    with open("config.json", "w") as json_file:
        json.dump(config_data, json_file, indent=4)

    return config

def vits_model_change(vits_model):
    """
    修改vits模型
    :param vits_model: vits模型
    :return:
    """
    config = Config()
    config.vits_model = vits_model
    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
        config_data["vits_model"] = config.vits_model

    with open("config.json", "w") as json_file:
        json.dump(config_data, json_file, indent=4)

    return config


def set_gpt_config_change(openai_api_key_input, openai_api_url_input, cosplay_role_input, prompts_path_input, openai_chat_mode_input):
    """
    修改gpt配置
    :param openai_api_key_input: openai的key
    :param openai_api_url_input: openai的url
    :param cosplay_role_input: 扮演的角色
    :param prompts_path_input: prompts的路径
    :return:
    """
    config = Config()

    config.openai_api_key = openai_api_key_input
    config.openai_api_url = openai_api_url_input
    config.cosplay_role = cosplay_role_input
    config.prompts_path = prompts_path_input
    config.openai_chat_mode = openai_chat_mode_input

    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
        config_data["openai_config"]["openai_api_key"] = config.openai_api_key
        config_data["openai_config"]["openai_api_url"] = config.openai_api_url
        config_data["openai_config"]["cosplay_role"] = config.cosplay_role
        config_data["openai_config"]["prompts_path"] = config.prompts_path
        config_data["openai_config"]["openai_chat_mode"] = config.openai_chat_mode

    with open("config.json", "w") as json_file:
        json.dump(config_data, json_file, indent=4)

    return config


def gpt_model_change(gpt_model):
    """
    修改gpt模型
    :param gpt_model: gpt模型
    :return:
    """
    config = Config()
    config.gpt_model = gpt_model
    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
        config_data["gpt_model"] = config.gpt_model

    with open("config.json", "w") as json_file:
        json.dump(config_data, json_file, indent=4)

    return config

config = Config()
