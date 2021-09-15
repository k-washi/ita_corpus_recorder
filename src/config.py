import os
import sys
from hydra import initialize_config_dir, compose

class Config():
    """
    hydraによる設定値の取得 (conf)
    """
    @staticmethod
    def get_cnf(conf_path: str):
        """
        設定値の辞書を取得
        @param
            conf_path: str
        @return
            cnf: OmegaDict
        """
        conf_dir = os.path.join(os.getcwd(), conf_path)
        if not os.path.isdir(conf_dir):
            raise FileExistsError(f"{conf_dir}が存在しませんでした。")
            sys.exit(-1)

        with initialize_config_dir(config_dir=conf_dir):
            cnf = compose(config_name="default.yaml")
            return cnf

if __name__ == "__main__":
    cnf = Config.get_cnf("./config")
    print(cnf)