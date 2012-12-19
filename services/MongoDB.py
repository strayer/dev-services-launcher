# coding=utf-8
import subprocess
import os
import ctypes
import settings

class MongoDB(object):
    def __init__(self):
        self.path = settings.MONGODB_CWD
        self.executable = settings.MONGODB_EXECUTABLE
        self.client_executable = settings.MONGODB_CLIENT_EXECUTABLE
        self.config_path = settings.MONGODB_CONF

    def start(self):
        with open(os.devnull, "w") as fnull:
            self.process = subprocess.Popen(
                args = [self.executable, '--config', self.config_path],
                cwd = self.path,
                stdout = fnull
            )

    def stop(self,):
        with open(os.devnull, "w") as fnull:
            stop_process = subprocess.Popen(
                args = [self.client_executable, 'localhost/admin', '--eval', 'db.shutdownServer();'],
                cwd = self.path,
                stdout = fnull
            )

            self.process.wait()
            stop_process.wait()

    def __str__(self):
        args = [self.executable, '--config', self.config_path, '--version']

        proc = subprocess.Popen(args=args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        return ", ".join(stdout.strip().decode('utf-8').splitlines())
