import subprocess

class CommandOp:
    def __init__(self, command, params):
        self.command = command
        self.params = params
        self.exit_code = None

    def should_skip(self):
        return False

    def check_ready(self):
        ## Todo check that command exists e.g. `which command` returns something
        return True

    def run(self):
        args = [self.command]
        args.extend(self.params)
        print("Running: %s" % ' '.join(args))
        self.exit_code = subprocess.call(args)
        pass 

    def was_success(self):
        return self.exit_code == 0

    def step_name(self):
        return "run command %s" % self.command
