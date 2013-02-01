# coding=utf-8
import glob
import re
import subprocess
import os
import settings
import threading
import sys
import time

class MongoDB(object):
    def __init__(self):
        self.path = settings.MONGODB_CWD
        self.executable = settings.MONGODB_EXECUTABLE
        self.client_executable = settings.MONGODB_CLIENT_EXECUTABLE
        self.config_path = settings.MONGODB_CONF

        self.touch_thread = None
        self.abort_db_touch = False
        self.dbpath = None

        if not os.path.exists(self.config_path):
            sys.exit("Could not find MongoDB config at path "+self.config_path)

        if settings.MONGODB_PERIODICALLY_TOUCH_DB_FILES:
            with open(self.config_path, 'r') as conf:
                regex = re.compile('dbpath\s*=\s*(.+)\s*$')
                for line in conf:
                    r = regex.match(line)
                    if r:
                        self.dbpath = r.groups()[0]

                        if not os.path.isabs(self.dbpath):
                            self.dbpath = os.path.join(self.path, self.dbpath)

            if not self.dbpath or not os.path.exists(self.dbpath):
                print('Warning! Could not find MongoDB dbpath!')
                print('Automatic touch of db files disabled.')

    def start(self):
        with open(os.devnull, "w") as fnull:
            self.process = subprocess.Popen(
                args = [self.executable, "--config", self.config_path],
                cwd = self.path,
                stdout = fnull
            )

            if settings.MONGODB_PERIODICALLY_TOUCH_DB_FILES and self.dbpath:
                    if not self.touch_thread:
                        self.touch_thread = threading.Thread(target=self.db_touch)
                    self.abort_db_touch = False
                    self.touch_thread.start()

    def stop(self,):
        with open(os.devnull, "w") as fnull:
            stop_process = subprocess.Popen(
                args = [self.client_executable, "localhost/admin", "--eval", "db.shutdownServer();"],
                cwd = self.path,
                stdout = fnull
            )

            if settings.MONGODB_PERIODICALLY_TOUCH_DB_FILES:
                self.abort_db_touch = True

            self.process.wait()
            stop_process.wait()
            if settings.MONGODB_PERIODICALLY_TOUCH_DB_FILES:
                self.touch_thread.join()
                # One last touch since there should be no more permission errors
                self.db_touch()

    def db_touch_loop(self):
        while not self.abort_db_touch:
            self.db_touch()
            time.sleep(5)

    def db_touch(self):
        data_files = glob.glob(os.path.join(self.dbpath, '*.[0-9]*'))
        data_files+= glob.glob(os.path.join(self.dbpath, '*.ns'))

        for file in data_files:
            path = os.path.join(self.dbpath, file)
            if os.path.exists(path):
                try:
                    os.utime(path)
                except PermissionError as e:
                    # Ignore permission errors when somebody else openend the file
                    # (propably MongoDB... still have to investigate this)
                    if e.winerror != 32:
                        raise

    def __str__(self):
        args = [self.executable, "--config", self.config_path, "--version"]

        proc = subprocess.Popen(args=args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        return ", ".join(stdout.strip().decode("utf-8").splitlines())
