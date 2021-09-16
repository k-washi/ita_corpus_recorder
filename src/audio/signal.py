import sys
import pathlib

root_path = pathlib.Path(__file__, "..", "..", "..").resolve()
print(root_path)
if root_path not in sys.path:
    sys.path.append(str(root_path))

import pyaudio
import wave
import time
import sys
import numpy as np
import struct
from src.audio.device import Microphone

# -------- Utils -----------------

def convPa2np(data,channelNum):
    """
    [0, 1, 2, 3, 4, 5] 
    =>.reshape([2,3]) 
    [[0,1,2],[3,4,5]]
    =>.reshape([フレーム数, チャンネル数]).T （転置 または、order オプションを使用する）
    """
    return data.reshape([-1, channelNum]).T

def convNp2pa(data):
    """
    b (チャンネル数 x フレーム数)
    array([[0, 3],
            [1, 4],
            [2, 5]])＝
    >>> b.reshape([-1])
    array([0, 3, 1, 4, 2, 5])
    >>> b.T.reshape([-1])
    array([0, 1, 2, 3, 4, 5])
    """
    return data.T.reshape([-1]) 



class AudioProcessing():
    def __init__(self, in_mic: Microphone, out_mic: Microphone, cnf) -> None:
        self.pAudio = pyaudio.PyAudio()

        self.in_mic = in_mic
        self.out_mic = out_mic
        self.cnf = cnf
        self.sampling_rate = cnf.audio.sampling_rate
        self.sampling_size_byte = int(cnf.audio.sample_bit / 8)
        self.start_trim_sec = cnf.audio.start_trim_sec
        self.end_tirm_sec = cnf.audio.end_trim_sec
        self.chunk = cnf.audio.stream_chunk

        if self.sampling_size_byte == 2:
            self.format = pyaudio.paInt16
            self.dtype = np.int16
        elif self.sampling_size_byte == 4:
            self.format = pyaudio.paInt32
            self.dtype = np.int32
            print("現在対応していないサンプリングサイズです。")
            sys.exec(-1)

        self.__record_list = []
        self.__output_channel_num = 1

        self.data = np.zeros((int(self.chunk)), dtype=self.dtype)
        self.npData = np.zeros((self.__output_channel_num, int(self.chunk)), dtype=self.dtype)
        self.outData = np.zeros((self.__output_channel_num * self.chunk), dtype=self.dtype)
        self.listenData = np.zeros((self.chunk * 2), dtype=self.dtype)
        self.wf = None

        self.listen_mode = False
        self.record_mode = False
    
    def callback(self, in_data, frame_count, time_info, status):
        if time.time() - self.start_time < self.start_trim_sec:
            out_data = self.outData.tobytes()
            return (out_data, pyaudio.paContinue)
        
        # 入力をchannelごとに分割し、1chだけ取り出す
        data = convPa2np(np.frombuffer(in_data, self.dtype), channelNum=self.in_mic.in_channel_num)[0, :] #ch1 input
        if data[data > 0].sum() == 0:
            print("Audio record stream empty.")
        self.npData[:, :] = data
        # フラットなデータに変換
        self.outData[:] = convNp2pa(self.npData)

        self.__record_list += self.outData.tolist()
        out_data = self.outData.tobytes()
        return (out_data, pyaudio.paContinue)


    def reset(self):
        self.__record_list = []
    
    def record_start(self):
        self.start_time = time.time()
        self.reset()

        if self.listen_mode:
            self.listen_stop()
        self.record_mode = True

        """
        rate – Sampling rate
        channels – Number of channels
        format – Sampling size and format. See PortAudio Sample Format.
        input – Specifies whether this is an input stream. Defaults to False.
        output – Specifies whether this is an output stream. Defaults to False.
        input_device_index – Index of Input Device to use. Unspecified (or None) uses default device. Ignored if input is False.
        output_device_index – Index of Output Device to use. Unspecified (or None) uses the default device. Ignored if output is False.
        frames_per_buffer – Specifies the number of frames per buffer.
        start – Start the stream running immediately. Defaults to True. In general, there is no reason to set this to False.
        input_host_api_specific_stream_info – Specifies a host API specific stream information data structure for input.
        output_host_api_specific_stream_info – Specifies a host API specific stream information data structure for output.
        stream_callback –Specifies a callback function for non-blocking (callback) operation. Default is None, which indicates blocking operation (i.e., Stream.read() and Stream.write()). To use non-blocking operation, specify a callback that conforms to the following signature:
        callback(in_data,      # recorded data if input=True; else None
                frame_count,  # number of frames
                time_info,    # dictionary
                status_flags) # PaCallbackFlags
        time_info is a dictionary with the following keys: input_buffer_adc_time, current_time, and output_buffer_dac_time; see the PortAudio documentation for their meanings. status_flags is one of PortAutio Callback Flag.
        The callback must return a tuple:
        (out_data, flag)
        out_data is a byte array whose length should be the (frame_count * channels * bytes-per-channel) if output=True or None if output=False. flag must be either paContinue, paComplete or paAbort (one of PortAudio Callback Return Code). When output=True and out_data does not contain at least frame_count frames, paComplete is assumed for flag.
        """
        self.stream = self.pAudio.open(
            format = self.format,
            rate = self.sampling_rate, 
            channels = self.in_mic.in_channel_num,
            input = True,
            output = False,
            input_device_index = self.in_mic.index,
            #output_device_index = self.out_mic.index,
            stream_callback = self.callback,
            frames_per_buffer = self.chunk
        )

        self.stream.start_stream()
        
    
    def record_stop(self):
        self.stream.stop_stream()
        self.stream.close()
        print("record stop")
        self.record_mode = False

    
    def save(self, wav_path):
        if self.listen_mode:
            self.listen_stop()
        if self.record_mode:
            self.record_stop()

        if len(self.__record_list) == 0:
            print(f"録音結果は空です。")
            return False, None

        cut_index = int(self.end_tirm_sec * self.sampling_rate)
        if len(self.record_list) > cut_index:
            output_data = self.record_list[:-cut_index]
        else:
            output_data = self.record_list
        
        data = struct.pack('h' * len(output_data), *output_data)
        print(len(self.__record_list)/self.sampling_rate)
        print(self.__record_list[-10:])
        with wave.open(wav_path, "wb") as ww:
            ww.setnchannels(self.__output_channel_num)
            ww.setsampwidth(self.sampling_size_byte)
            ww.setframerate(self.sampling_rate)
            ww.writeframes(data)
        
        print(f"{wav_path}を保存しました。")
        return True, output_data
    
    def listen_callback(self, in_data, frame_count, time_info, status):
        if self.wf is not None:
            data = self.wf.readframes(frame_count)
            if len(data) == 0:
                return ("", pyaudio.paComplete)
            return (data, pyaudio.paContinue)

        return ("", pyaudio.paComplete)
        
    
    def open_and_listen(self, wav_path):
        if self.record_mode:
            self.record_stop()
        self.listen_mode = True
        self.wf = wave.open(wav_path, "rb")
        
        self.listen_stream = self.pAudio.open(format=self.pAudio.get_format_from_width(self.wf.getsampwidth()),
                            channels=self.wf.getnchannels(),
                            rate=self.wf.getframerate(),
                            stream_callback=self.listen_callback,
                            output_device_index=self.out_mic.index,
                            output=True)
        self.listen_stream.start_stream()
    
    def listen_stop(self):
        self.listen_stream.stop_stream()
        self.listen_stream.close()
        if self.wf is not None:
            self.wf.close()
        
        self.listen_mode = False
                

    @property
    def record_list(self):
        return self.__record_list
    
    def __del__(self):
        self.pAudio.terminate()




if __name__ == "__main__":
    from src.audio.device import AudioDevice
    from src.config import Config

    cnf = Config.get_cnf("config")
    print(cnf)
    in_mic = AudioDevice.get_audio_device_info(0)
    out_mic = AudioDevice.get_audio_device_info(1)

    aP = AudioProcessing(in_mic, out_mic, cnf)

    # 録音
    print("start")
    aP.record_start()
    time.sleep(2)
    aP.record_stop()
    print("stop")
    
    
    aP.save("./tmp.wav")
    aP.open_and_listen("./tmp.wav")
    time.sleep(5)
    aP.listen_stop()

    print(in_mic)
    print(out_mic)

