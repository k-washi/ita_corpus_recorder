import os


def load_corpus(file_path):
    """
    ita corpusのファイルを読みこむ

    return
    ['EMOTION100_001:えっ嘘でしょ。,エッウソデショ。\n', 
    'EMOTION100_002:シュヴァイツァーは見習うべき人間です。,シュヴァイツァーワミナラウベキニンゲンデス。\n', 
    ...]
    """
    if not os.path.exists(file_path):
        raise FileExistsError(f"{file_path}は存在しません.")
    with open(file_path, "r") as f:
        datalist = f.readlines()
    
    return sorted(datalist)

def split_corpus(corpus_list):
    """
    corpusの分割
    [['EMOTION100_001', 'えっ嘘でしょ。', 'エッウソデショ。'],
    """
    corput_split_list = []
    for corpus in corpus_list:
        corpus = corpus.replace("\n", "")
        index, text = corpus.split(":")
        kannjikanamajiri, kana = text.split(",")
        corput_split_list.append(
            [index, kannjikanamajiri, kana]
        )
    return corput_split_list







if __name__ == "__main__":
    data_path = "./ita-corpus/emotion_transcript_utf8.txt"
    res = load_corpus(data_path)
    print(len(res))
    print(res[:5])

    res = split_corpus(res)
    print(res[:2])