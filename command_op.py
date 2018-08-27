import subprocess

class CommandOp:
    def __init__(self, command, params):
        self.command = command
        self.params = params
        self.exit_code = None

    def check_ready(self):
        return True

    def run(self):
        args = list(command)
        args.extend(params)
        self.exit_code = subprocess.call(args)
        pass 

    def was_success(self):
        return self.exit_code == 0
