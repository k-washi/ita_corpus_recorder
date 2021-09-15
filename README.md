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