class CommandOp:
    def __init__(self, path, file_strategy, **config_dict):
        self.path = path;
        self.config_dict = config_dict
        self.file_strategy = file_strategy
        pass

    def check_ready(self):
        pass

    def run(self):
        pass 

    def was_success(self):
        pass

    def handle_error(self):
        pass
