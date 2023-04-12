
import os
import pytest

from random import randint

from semaphore_lock.lock import FileLock

def describe_file_lock():
    def test_lock_acquire_release():
        lock_path = "./._tmp_.lock"
        if os.path.exists(lock_path):
            os.remove(lock_path)
        file_lock = FileLock(lock_path)
        assert file_lock.acquire()
        assert not file_lock.acquire()
        assert file_lock.release()
        assert not file_lock.release()

    def test_host_id():
        lock_path = "./._tmp_.lock"
        file_lock = FileLock(lock_path)
        id = randint(9, 99999)
        file_lock.set_machine_id(id)
        assert id == file_lock.machine_id

    


