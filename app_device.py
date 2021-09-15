from src.audio.device import AudioDevice

device_list = AudioDevice.get_audio_devices_info()
print("")
for device in device_list:
    
    print(device)
    print("")