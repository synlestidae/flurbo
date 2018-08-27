import subprocess

class CreateDirOp:
    def __init__(self, dirs):
        self.dirs = dirs
        self.progress = 0
        pass

    def check_ready(self):
        return True

    def run(self):
        self.progress = 0
        for d in self.dirs:
            if subprocess.call(['mkdir', '-p', d]) > 0:
                return
            self.progress += 1

    def was_success(self):
        self.progress < len(self.dirs)
