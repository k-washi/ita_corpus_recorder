import os
from glob import glob

# 録音済みのデータのindexを出力
def get_recorded_index(cnf):
    recorded_dir = os.path.join(cnf.path.record_dir, cnf.path.recorded_dir)
    files = glob(recorded_dir + "/*")
    return [os.path.splitext(os.path.basename(file))[0] for file in files]

# 評価済みのデータのindexを出力
def get_eval_index(cnf): 
    eval_dir = os.path.join(cnf.path.record_dir, cnf.path.eval_dir)
    files = glob(eval_dir + "/*")
    return [os.path.splitext(os.path.basename(file))[0] for file in files]

    