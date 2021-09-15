import os
import sys
import tkinter as tk
from tkinter import messagebox
import argparse

from src.record_frame import RecordFrame
from src.config import Config

from src.audio.device import AudioDevice, Microphone

RECORDED_DIR = "recorded"
EVAL_DIR = "eval"

class Application(tk.Frame):
    def __init__(self, master, args, cnf):
        super().__init__(master)
        self.pack()

        self.cnf = cnf

        self.mic = self.get_audio_deivce(args.device)

        # 画面の初期設定
        
        self.master.geometry("1300x300")
        self.master.title("ITA Corpus Recorder")

        self.create_widgets()
    
    def get_audio_deivce(self, mic_id) -> Microphone:
        mic = AudioDevice.get_audio_device_info(mic_id)
        if mic is None:
            res = messagebox.showerror("Micの設定エラー", f"マイク{mic_id}のマイクは存在しません。")
            if res == "ok":
                sys.exit(-1)
        
        print(mic)
        if self.cnf.audio.sampling_rate > mic.sampling_rate:
            res = messagebox.showerror("Micの設定エラー", f"マイク{mic_id}:{mic.name}には、{self.cnf.audio.sampling_rate}Hzを録音する能力がありません。({mic.sampling_rate})Hz以下に設定してください。")
            if res == "ok":
                sys.exit(-1)
        
        if mic.in_channel_num == 0:
            res = messagebox.showerror("Micの設定エラー", f"マイク{mic_id}:{mic.name}は、入力を受け付けていません。")
            if res == "ok":
                sys.exit(-1)
        
        return mic
            

    
    def create_widgets(self):
        self.mic_label = tk.Label(self, text=f"マイク情報: {str(self.mic)}").grid(row=0, column=0, columnspan=3)
        self.record_label = tk.Label(self, text=f"収録情報: SampleRate: {self.cnf.audio.sampling_rate} | Sample size: {self.cnf.audio.sample_bit} bit").grid(row=1, column=0, columnspan=3)

        self.record_frame = RecordFrame(self, self.cnf).grid(row=2, column=0)
        self.record_frame2 = RecordFrame(self, self.cnf).grid(row=2, column=1)

    def callBack(self):
        pass

def main(args):
    cnf = Config.get_cnf(args.config)
    # パスなどの初期設定
    os.makedirs(cnf.path.record_dir, exist_ok=True)
    os.makedirs(os.path.join(cnf.path.record_dir, cnf.path.recorded_dir), exist_ok=True)
    os.makedirs(os.path.join(cnf.path.record_dir, cnf.path.eval_dir), exist_ok=True)

    # app立ち上げ
    root = tk.Tk()
    app = Application(root, args, cnf)
    app.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, default="config")
    parser.add_argument("--device", "-d", type=int, default=0)
    
    args = parser.parse_args()
    main(args)