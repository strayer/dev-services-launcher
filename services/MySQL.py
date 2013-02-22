# coding=utf-8
import subprocess
import os
import settings
import sys

class MySQL(object):
    def __init__(self):
        self.path = settings.MYSQL_CWD
        self.executable = settings.MYSQLD_EXECUTABLE
        self.mysqladmin_executable = settings.MYSQLADMIN_EXECUTABLE
        self.mysqladmin_parameters = settings.MYSQLADMIN_PARAMS
        self.config_path = settings.MYSQL_CONF

        if not os.path.exists(self.config_path):
            sys.exit("Could not find MySQL config at path "+self.config_path)

    def start(self):
        with open(os.devnull, "w") as fnull:
            self.process = subprocess.Popen(
                args = [
                    self.executable,
                    '--defaults-file={}'.format(self.config_path),
                    '-b', self.path
                ],
                cwd = self.path,
                stdout = fnull
            )

    def stop(self,):
        stop_process = subprocess.Popen(
            args = [self.mysqladmin_executable] +
                   self.mysqladmin_parameters +
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

        return output[output.find('.exe')+4:].strip()
