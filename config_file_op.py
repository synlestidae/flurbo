import os

class ConfigFileOp:
    def __init__(self, path, file_strategy, **config_dict):
        self.path = path;
        self.config_dict = config_dict
        self.file_strategy = file_strategy
        pass

    def check_ready(self):
        try:
            f = open(self.path, 'r')
        except IOError as e:
            print(e)
            return False
        finally:
            f.close()
            return True

    def run(self):
        with self.file_strategy(self.path) as f:
            for k in self.config_dict:
                f[k] = self.config_dict

    def was_success(self):
        with self.file_strategy(self.path) as f:
            return all([f[k] == self.config_dict[k] for k in f])
