
import os
import pytest

from random import randint

from .lock import FileLock

LOCK_PATH = "./._tmp_.lock"

@pytest.fixture
def clean_up():
    if os.path.exists(LOCK_PATH):
        os.remove(LOCK_PATH)

def describe_file_lock():
    """"""
    def test_is_locked(clean_up):
        system_1 = FileLock(LOCK_PATH)
        system_1.set_machine_id(randint(9,99))
        system_2 = FileLock(LOCK_PATH)
        system_2.set_machine_id(randint(199,299))
        assert system_1.acquire()
        assert system_2.is_locked()
        assert system_1.is_locked()
        assert system_1.release()
        assert not system_1.is_locked()
        assert not system_2.is_locked()     

    def test_lock(clean_up):
        system_1 = FileLock(LOCK_PATH)
        system_1.set_machine_id(randint(9,99))
        system_2 = FileLock(LOCK_PATH)
        system_2.set_machine_id(randint(199,299))
        system_3 = FileLock(LOCK_PATH)
        system_3.set_machine_id(randint(399,499))
        assert system_1.acquire()
        assert not system_2.acquire()
        assert not system_3.acquire()

        assert not system_2.release()
        assert not system_3.release()
        assert system_1.release()

        assert system_2.acquire()
        assert not system_3.acquire()

    def test_release(clean_up):
        file_lock = FileLock(LOCK_PATH)
        assert file_lock.acquire()
        assert not file_lock.acquire()
        assert file_lock.release()
        assert not file_lock.release()

        assert file_lock.acquire()
        file_lock2 = FileLock(LOCK_PATH)
        file_lock2.set_machine_id(randint(99, 999))
        assert not file_lock2.release()
        assert file_lock2.release(force=True)
        assert not file_lock.release()

    def test_set_machine_id(clean_up):
        file_lock = FileLock(LOCK_PATH)
        id = randint(9, 99999)
        file_lock.set_machine_id(id)
        assert id == file_lock.machine_id

    def test_who_locked(clean_up):
        system_1 = FileLock(LOCK_PATH)
        system_1.set_machine_id(randint(9, 99))
        system_2 = FileLock(LOCK_PATH)
        system_2.set_machine_id(randint(100, 999))

        system_1.acquire()
        assert system_1.machine_id == system_1.who_locked()
        assert system_1.machine_id == system_2.who_locked()




        
    


