import subprocess
import os
from tools import win32_kill

class PHP(object):
    def __init__(self, php_path, addresses):
        self.path = php_path
        self.addresses = addresses
        self.processes = []

    def start(self):
        self.stop()
        for address in self.addresses:
            self.processes.append(
                subprocess.Popen(
                    args = [os.path.join(self.path, "php-cgi.exe"), "-b", address],
                    cwd = self.path
                )
            )

    def __str__(self):
        args = [os.path.join(self.path, "php-cgi.exe"), '--version']

        proc = subprocess.Popen(args=args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        stdout_lines = stdout.splitlines()

        return stdout_lines[0].decode('utf-8')

    def stop(self):
        for process in self.processes:
            win32_kill(process.pid)
        self.processes = []