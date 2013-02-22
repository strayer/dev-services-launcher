# coding=utf-8
import subprocess
import os
import settings

class Redis(object):
    def __init__(self):
        self.path = settings.REDIS_CWD
        self.executable = settings.REDIS_SERVER_EXECUTABLE
        self.redis_cli_executable = settings.REDIS_CLI_EXECUTABLE
        self.redis_cli_parameters = settings.REDIS_CLI_PARAMS

    def start(self):
        with open(os.devnull, "w") as fnull:
            self.process = subprocess.Popen(
                args = [
                    self.executable
                ],
                cwd = self.path,
                stdout = fnull
            )

    def stop(self,):
        stop_process = subprocess.Popen(
            args = [self.redis_cli_executable] +
                   self.redis_cli_parameters +
                   ["SHUTDOWN"],
            cwd = self.path
        )

        self.process.wait()
        stop_process.wait()

    def __str__(self):
        args = [self.executable, "--version"]

        proc = subprocess.Popen(args=args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        output = stdout.strip().decode("utf-8")

        return output.replace("Redis server version", "").strip()
