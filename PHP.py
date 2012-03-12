import subprocess
import os
import signal

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

    def stop(self):
        for process in self.processes:
            # process.terminate() gets an "Access denied" - no idea why...
            os.kill(process.pid, signal.CTRL_C_EVENT)
            process.wait()
        self.processes = []