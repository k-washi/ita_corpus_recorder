import os
import tkinter as tk
from tkinter import ttk
from src.load_corpus import load_corpus, split_corpus
from src.utils import get_eval_index, get_recorded_index
from src.audio.signal import AudioProcessing
import shutil
class RecordFrame(tk.Frame):
    def __init__(self, master, in_mic, out_mic, cnf):
        super().__init__(master)        
        self.cnf = cnf
        self.in_mic = in_mic
        self.out_mic = out_mic
        
        # 一時保存用のpathを作成
        os.makedirs(self.cnf.audio.tmp_dir, exist_ok=True)
        self._tmp_audio_path = os.path.join(self.cnf.audio.tmp_dir, self.cnf.audio.tmp_wav)

        self.audio_proc = AudioProcessing(self.in_mic, self.out_mic, self.cnf)
        
        self.recorded_dir = os.path.join(self.cnf.path.record_dir, self.cnf.path.recorded_dir)
        
        self.now_record_selected = -1
        self.now_record_index = ""
        self.recording = False
        self.has_recorded_audio = False
        self.listening = False

        self.create_text_widgets()
        self.create_list_box()
        self.create_widgets()
    
    def load_corpus(self):
        # コーパスの読み込み
        corpus1 = split_corpus(load_corpus(self.cnf.path.emotion_corpus))
        corpus2 = split_corpus(load_corpus(self.cnf.path.recitation_corpus))

        tmp_corpus = corpus1 + corpus2

        # 録音済みデータ、評価済みデータを除去
        recorded_index = get_recorded_index(self.cnf)
        # eval_index = get_eval_index(self.cnf)
        saved_index = recorded_index #+ eval_index

        corpus = {}
        for c in tmp_corpus:
            if c[0] in saved_index:
                continue
            corpus[c[0]] = c[1]
        print(len(corpus.keys()))
        return corpus

    def create_list_box(self):
        self.corpus_dic = self.load_corpus()

        listbox_init_corpus = tk.StringVar(value=list(self.corpus_dic.keys()))
        self.corpus_listbox = tk.Listbox(self, bd=5, width=15, relief="groove", fg="black",bg="white", selectmode="single", listvariable=listbox_init_corpus)

        self.corpus_listbox.grid(row=0, column=0, rowspan=3, columnspan=2, padx=5, pady=10)

        self.corpus_listbox.bind('<<ListboxSelect>>', self.listbox_active)

        
        self.active = False
        self.corpus_listbox.selection_clear(0, tk.END)
        self.corpus_listbox.selection_set(0)
        self.corpus_listbox.activate(0)
        self.text_update()



    def create_widgets(self):
        self.record_button = tk.Button(
            self,
            text="録音",
            command=self.record_start
        )
        self.record_button.grid(row=0, column=3, pady=20)
        self.record_button.config(fg="gray")



        self.stop_button = tk.Button(
            self,
            text="停止",
            command=self.record_stop
        )
        self.stop_button.grid(row=0, column=4, pady=20)
        self.stop_button.config(fg="gray")

        self.listen_button = tk.Button(
            self,
            text="聞く",
            command=self.listen_audio
        )
        self.listen_button.grid(row=0, column=5, pady=20)
        self.listen_button.config(fg="gray")

        self.publish_button = tk.Button(
            self,
            text="提出",
            command=self.publish_audio
        )
        self.publish_button.grid(row=0, column=6, pady=20)
        self.publish_button.config(fg="gray")
        

    def create_text_widgets(self):
        # text
        self.selected_var = tk.StringVar(self)
        self.selected_text = tk.Label(self, textvariable=self.selected_var, font=("", 20))
        self.selected_var.set("選択してください。")

        self.selected_des_var = tk.StringVar(self)
        self.selected_text_des = tk.Message(self, textvariable=self.selected_des_var, font=("", 15), width=100)
        self.selected_des_var.set("***")

        self.selected_text.grid(row=1, column=3, columnspan=4)
        self.selected_text_des.grid(row=2, column=3, columnspan=4, rowspan=2, sticky=tk.W+tk.S, padx=5, pady=5)

    def text_update(self):
        index = self.corpus_listbox.curselection()
        if len(index) == 0:
            return
        text = self.corpus_listbox.get(index)
        dis = self.corpus_dic.get(text, "hogehoge")
        self.selected_var.set(text)
        self.selected_des_var.set(dis)    
    
    def listbox_active(self, context):
        self.active = True
        if not self.recording and not self.has_recorded_audio:
            self.text_update()
            self.record_button.config(fg="white")
    
    def record_start(self):
        if self.active and not self.recording:
            print("Record")
            self.record_button.config(fg="gray")
            self.stop_button.config(fg="white")
            self.listen_button.config(fg="gray")
            self.publish_button.config(fg="gray")

            self.recording = True
            self.listening = False
            self.audio_proc.record_start()
            

            if not self.has_recorded_audio:
                # 選択が反映される

                self.now_record_selected = self.corpus_listbox.curselection()
                self.now_record_index = self.corpus_listbox.get(self.now_record_selected)

    def record_stop(self): 
        if self.active and self.recording and not self.listening:
            print("Stop")
            self.record_button.config(fg="white")
            self.stop_button.config(fg="gray")
            self.listen_button.config(fg="white")
            self.publish_button.config(fg="white")
           
            self.audio_proc.record_stop() 
            ok = self.audio_proc.save(self._tmp_audio_path) #一時保存
            if not ok:
                print("recordはemptyです！")

            self.recording = False
            self.has_recorded_audio = True
            
        
    
    def listen_audio(self):
        if self.active and not self.recording and self.has_recorded_audio:
            print("聞く。")
            self.listening = True
            self.audio_proc.open_and_listen(self._tmp_audio_path)
            
            
           
            

    def publish_audio(self):
        if self.active and not self.recording and self.has_recorded_audio:
            print("提出しました。")
            audio_path = os.path.join(self.recorded_dir, self.now_record_index+".wav")
            shutil.move(
                self._tmp_audio_path,
                audio_path
            )

            self.record_button.config(fg="white")
            self.stop_button.config(fg="gray")
            self.listen_button.config(fg="gray")
            self.publish_button.config(fg="gray")
            self.listening = False
            self.has_recorded_audio = False
            self.create_list_box()
        






        