#! python3
"""Distributed Lock Framework"""
import datetime
import json
import os
import socket
import time

from abc import ABC, abstractmethod

class Lock(ABC):
    @abstractmethod
    def acquire(self):
        pass
    
    @abstractmethod
    def release(self):
        pass
    
    @abstractmethod
    def is_locked(self):
        pass
    
    @abstractmethod
    def who_locked(self):
        pass


class FileLock(Lock):
    def __init__(self, lock_path='./_tmp_.lock'):
        self.lock_path = lock_path
        self.host_id = socket.gethostname()
        self.lock_data = {'owner': None, 'timestamp': None}
    
    @property
    def machine_id(self):
        return self.host_id

    def acquire(self):
        if self.is_locked():
            return False

        try:
            with open(self.lock_path, 'w') as lock_file:
                self.lock_data['owner'] = self.machine_id
                self.lock_data['timestamp'] = datetime.datetime.now().timestamp()
                json.dump(self.lock_data, lock_file)
            return True
        except FileExistsError:
            return False

    def is_locked(self):
        if os.path.exists(self.lock_path):
            return True

    def release(self, force=False):
        try:
            if self.who_locked() == self.machine_id or force:
                os.remove(self.lock_path)
                return True
        except FileNotFoundError:
            return False

    def set_machine_id(self, id=None):
        if id is not None:
            self.host_id = id

    def who_locked(self):
        if not self.is_locked():
            return None
        with open(self.lock_path, 'r') as lock_file:
            lock_data = json.load(lock_file)
            return lock_data['owner']

        