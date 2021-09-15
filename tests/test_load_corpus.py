from src.load_corpus import load_corpus, split_corpus

corpus_path = "./ita-corpus/emotion_transcript_utf8.txt"

def test_success():
    res = load_corpus(corpus_path)
    assert len(res) == 100
    assert res[0] == 'EMOTION100_001:えっ嘘でしょ。,エッウソデショ。\n'

    res = split_corpus(res)
    assert len(res) == 100
    assert len(res[0]) == 3
    assert res[0][0] == "EMOTION100_001"
    assert res[0][1] == "えっ嘘でしょ。"
    assert res[0][2] == "エッウソデショ。" 