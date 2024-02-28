from PyQt6.QtCore import QThread, pyqtSignal

import requests
import pyaudio
import wave

import config


class GptSoVitsThread(QThread):
    transcription_complete_gptsovits = pyqtSignal()
    error_occurred_gptsovits = pyqtSignal(str)

    def __init__(self, text, id="0", lang="auto", prompt_lang="auto", preset="default"):
        super().__init__()
        self.text = text
        self.id = id
        self.lang = lang
        self.prompt_lang = prompt_lang
        self.preset = preset
        self.config_gptSoVits_wav_path = config.Config()
        self.error_flag = False

    def run(self):
        self.gptSoVits_textToVodie()
        if not self.error_flag:
            self.play_audio()
        self.transcription_complete_gptsovits.emit()

    def gptSoVits_textToVodie(self):
        self.config_gptSoVits_wav_path = config.Config()
        url = self.config_gptSoVits_wav_path.gptSoVits_api_url
        params = {
            "text": self.text,
            "id": self.id,
            "lang": self.lang,
            "prompt_lang": self.prompt_lang,
            "preset": self.preset,
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                audio_data = response.content
                with open(self.config_gptSoVits_wav_path.gptSoVits_wav_path, "wb") as f:
                    f.write(audio_data)
                print("音频文件已保存")
            else:
                print("请求失败，状态码为", response.status_code)
                return
        except Exception as e:
            print(e)
            # 弹出提示框
            self.error_flag = True
            self.error_occurred_gptsovits.emit("请求失败，请检查GPT-SoVITS连接！")
            return

    def play_audio(self):
        self.config_gptSoVits_wav_path = config.Config()
        with wave.open(self.config_gptSoVits_wav_path.gptSoVits_wav_path, 'rb') as f:
            nchannels, sampwidth, framerate, nframes, comptype, compname = f.getparams()
            data = f.readframes(nframes)

        p = pyaudio.PyAudio()
        stream = None
        try:
            stream = p.open(format=p.get_format_from_width(sampwidth),
                            channels=nchannels,
                            rate=framerate,
                            output=True)
            stream.write(data)
        except Exception as e:
            print(e)
            return
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
