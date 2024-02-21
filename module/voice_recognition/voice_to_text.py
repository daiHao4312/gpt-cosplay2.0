import pyaudio
import wave
import speech_recognition as sr
from PyQt6.QtCore import QThread, pyqtSignal


class AudioRecorderThread(QThread):
    audio_finished = pyqtSignal()  # 定义信号

    def __init__(self, wave_out_path):
        super().__init__()
        self.wave_out_path = wave_out_path
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.p = None
        self.stream = None
        self.transcribed_text = None

    def run(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        wf = wave.open(self.wave_out_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        print("录音准备就绪...")

        frames = []
        while not self.isInterruptionRequested():
            data = self.stream.read(self.CHUNK)
            frames.append(data)

        wf.writeframes(b''.join(frames))
        wf.close()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self.audio_finished.emit()  # 发射信号

    def stop_recording(self):
        self.requestInterruption()  # 请求中断

    def transcribe_audio(self):
        r = sr.Recognizer()
        with sr.AudioFile(self.wave_out_path) as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            audio = r.record(source)
        try:
            self.transcribed_text = r.recognize_google(audio, language='zh_CN', show_all=False)
        except Exception as e:
            print(e)


    def get_transcribed_text(self):
        return self.transcribed_text



