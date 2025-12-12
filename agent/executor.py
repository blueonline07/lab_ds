import subprocess


class Executor:
    def __init__(self, server_addr, cmd):
        self.proc = None
        self.cmd = cmd
        self.server_addr = server_addr

    def exec(self, command):
        print(command)

    def _start(self):
        self.proc = subprocess.Popen(self.cmd)

    def _stop(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()

    def _restart(self):
        self._stop()
        self._start()
