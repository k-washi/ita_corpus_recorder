from dataclasses import dataclass
import pyaudio
import wave

@dataclass
class Microphone:
    index: int
    name: str
    in_channel_num: int
    out_channel_num: int
    sampling_rate: int

    def __str__(self) -> str:
        return f"Index: {self.index} | Name: {self.name} | ChannelNum: in {self.in_channel_num} out {self.out_channel_num} | SampleRate: {int(self.sampling_rate)} Hz"




class AudioDevice():
    def __init__(self):
        pass
        

    @staticmethod
    def get_audio_devices_info():
        pAudio = pyaudio.PyAudio()
        device_list = []
        for i in range(pAudio.get_device_count()):
            device_info = pAudio.get_device_info_by_index(i)
            mic = Microphone(
                index=device_info['index'],
                name=device_info['name'],
                in_channel_num=device_info["maxInputChannels"],
                out_channel_num=device_info["maxOutputChannels"],
                sampling_rate=device_info["defaultSampleRate"]
            )

            device_list.append(mic)

        return device_list
    
    def get_audio_device_info(mic_id):
        pAudio = pyaudio.PyAudio()
        for i in range(pAudio.get_device_count()):
            device_info = pAudio.get_device_info_by_index(i)
            index = device_info['index']
            mic = Microphone(
                index=index,
                name=device_info['name'],
                in_channel_num=device_info["maxInputChannels"],
                out_channel_num=device_info["maxOutputChannels"],
                sampling_rate=device_info["defaultSampleRate"]
            )

            if index == mic_id:
                return mic
        return None

            