from PyQt6.QtCore import QThread, pyqtSignal

import requests
import pyaudio
import wave

import config


class VITSThread(QThread):
    transcription_complete = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, text, id="225", lang="zh", length="1.4"):
        super().__init__()
        self.text = text
        self.id = id
        self.lang = lang
        self.length = length
        self.config_vits_wav_path = config.Config()
        self.error_flag = False

    def run(self):
        self.vits_textToVodie()
        if not self.error_flag:
            self.play_audio()
        self.transcription_complete.emit()

    def vits_textToVodie(self):
        self.config_vits_wav_path = config.Config()
        url = self.config_vits_wav_path.vits_api_url
        params = {
            "text": self.text,
            "id": self.id,
            "lang": self.lang,
            "length": self.length,
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                audio_data = response.content
                with open(self.config_vits_wav_path.vits_wav_path, "wb") as f:
                    f.write(audio_data)
                print("音频文件已保存")
            else:
                print("请求失败，状态码为", response.status_code)
                return
        except Exception as e:
            print(e)
            # 弹出提示框
            self.error_flag = True
            self.error_occurred.emit("请求失败，请检查vits连接！")
            return

    def play_audio(self):
        self.config_vits_wav_path = config.Config()
        with wave.open(self.config_vits_wav_path.vits_wav_path, 'rb') as f:
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
