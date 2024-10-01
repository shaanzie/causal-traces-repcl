class FileProcessor:

    def __init__(self, cfg: dict) -> None:
        
        self.cfg = cfg
        # print('Configuration loaded.')
        # for key in cfg.keys():
        #     print('{} = {}'.format(key, cfg[key]))