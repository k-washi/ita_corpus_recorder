# ita_corpus_recorder
ITAコーパス 録音用

```
 git clone https://github.com/k-washi/ita_corpus_recorder.git
 --recursive
```

```
--recursive
```
をつけ忘れたら

```
git submodule update --init
```

```
pip install -r requirements.txt
```

# 実行

使用できるデバイスの一覧を表示
```
python app_device.py

Index: 0 | Name: Built-in Microphone | ChannelNum: in 2 out 0 | SampleRate: 44100 Hz
Index: 1 | Name: Built-in Output | ChannelNum: in 0 out 2 | SampleRate: 44100 Hz
Index: 2 | Name: DisplayPort | ChannelNum: in 0 out 2 | SampleRate: 48000 Hz
Index: 3 | Name: HyperX Quadcast | ChannelNum: in 0 out 2 | SampleRate: 48000 Hz
Index: 4 | Name: HyperX Quadcast | ChannelNum: in 2 out 0 | SampleRate: 48000 Hz
```

録音(-i マイク, -o 出力デバイス)
```
python app.py -i 4 -o 1
```

# config

config/audio/default.yaml
```
start_trim_sec: 0.1 # 録音時に最初に切り取る時間
end_trim_sec: 0.3 # 録音時に最後を切り取る時間
```
で、クリック音とか消すようにしている。

config/path/default.yaml
```
record_dir: data
```
保存するパス設定している

# Mac install

```
brew install portaudio
```

# test

```
pytest
```

# error

## in mac

```
    import _tkinter # If this fails your Python may not be configured for Tk
ModuleNotFoundError: No module named '_tkinter'
```

[Install tkinter on macOS](https://blog.lanzani.nl/2020/install-tkinter-macos/)


## 音声データが入力されない

ターミナルにマイクへの権限が当てられているか確認する。
また、VSCodeからではなく、ターミナルから実行する。

## ボタンの配置などがおかしい (動かない in mac)

[](https://stackoverflow.com/questions/60469202/unable-to-install-tkinter-with-pyenv-pythons-on-macos/60469203#60469203)
の Here is step by step guide **
で最後、以下のコマンドなるようにインストールしたところ、動いた！
```
env PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I/usr/local/opt/tcl-tk/include' --with-tcltk-libs='-L/usr/local/opt/tcl-tk/lib -ltcl8.6 -ltk8.6' --enable-shared" pyenv install 3.8.5
```