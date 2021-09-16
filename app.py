import os
import sys
import tkinter as tk
from tkinter import messagebox
import argparse

from src.record_frame import RecordFrame
from src.config import Config

from src.audio.device import AudioDevice, Microphone
from typing import List, Tuple

RECORDED_DIR = "recorded"
EVAL_DIR = "eval"

class Application(tk.Frame):
    def __init__(self, master, args, cnf):
        super().__init__(master)
        self.pack()

        self.cnf = cnf

        self.in_mic, self.out_mic = self.get_audio_deivce(args.in_device, args.out_device)

        # 画面の初期設定
        
        self.master.geometry("900x300+20+20")
        self.master.title("ITA Corpus Recorder")

        self.create_widgets()
    
    def get_audio_deivce(self, in_mic_id, out_mic_id) -> Tuple[Microphone, Microphone]:
        """in mic"""
        in_mic = AudioDevice.get_audio_device_info(in_mic_id)
        if in_mic is None:
            res = messagebox.showerror("InputMicの設定エラー", f"マイク{in_mic_id}のマイクは存在しません。")
            if res == "ok":
                sys.exit(-1)

        print(in_mic)
        if self.cnf.audio.sampling_rate > in_mic.sampling_rate:
            res = messagebox.showerror("InputMicの設定エラー", f"マイク{in_mic_id}:{in_mic.name}には、{self.cnf.audio.sampling_rate}Hzを録音する能力がありません。({in_mic.sampling_rate})Hz以下に設定してください。")
            if res == "ok":
                sys.exit(-1)
        
        if in_mic.in_channel_num == 0:
            res = messagebox.showerror("InputMicの設定エラー", f"マイク{in_mic_id}:{in_mic.name}は、入力を受け付けていません。")
            if res == "ok":
                sys.exit(-1)
            
        """out mic"""
        out_mic = AudioDevice.get_audio_device_info(out_mic_id)
        if out_mic is None:
            res = messagebox.showerror("OutputMicの設定エラー", f"マイク{out_mic_id}のマイクは存在しません。")
            if res == "ok":
                sys.exit(-1)

        print(out_mic)
        if self.cnf.audio.sampling_rate > out_mic.sampling_rate:
            res = messagebox.showerror("OutputMicの設定エラー", f"マイク{out_mic_id}:{out_mic.name}には、{self.cnf.audio.sampling_rate}Hzを再生する能力がありません。({out_mic.sampling_rate})Hz以下に設定してください。")
            if res == "ok":
                sys.exit(-1)
        
        if out_mic.out_channel_num == 0:
            res = messagebox.showerror("OutputMicの設定エラー", f"マイク{out_mic_id}:{out_mic.name}は、出力を受け付けていません。")
            if res == "ok":
                sys.exit(-1)


        """設定"""
        if self.cnf.audio.sample_bit != 16:
            res = messagebox.showerror("設定ファイルエラー", f"サンプリングサイズ: {self.cnf.audio.sample_bit}は、16 bitのみに対応しています。")
            if res == "ok":
                sys.exit(-1)
        
        return in_mic, out_mic
            

    
    def create_widgets(self):
        self.mic_label = tk.Label(self, text=f"入力デバイス情報: {str(self.in_mic)}").grid(row=0, column=0, columnspan=3)
        self.mic_label = tk.Label(self, text=f"出力デバイス情報: {str(self.out_mic)}").grid(row=1, column=0, columnspan=3)
        self.record_label = tk.Label(self, text=f"収録情報: SampleRate: {self.cnf.audio.sampling_rate} | Sample size: {self.cnf.audio.sample_bit} bit").grid(row=2, column=0, columnspan=3)

        self.record_frame = RecordFrame(self, self.in_mic, self.out_mic, self.cnf).grid(row=3, column=0)

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
    parser.add_argument("--in_device", "-i", type=int, default=0)
    parser.add_argument("--out_device", "-o", type=int, default=1)
    
    args = parser.parse_args()
    main(args)