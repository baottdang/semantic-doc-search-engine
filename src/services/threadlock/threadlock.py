import threading

class RWLock:
    def __init__(self):
        self._readers = 0
        self._readers_lock = threading.Lock()
        self._resource_lock = threading.Lock()

    def acquire_read(self):
        # Reader lock ensures that only one reader enables the condition in which resource lock is acquired
        with self._readers_lock:
            self._readers += 1
            if self._readers == 1:
                self._resource_lock.acquire()

    def release_read(self):
        with self._readers_lock:
            self._readers -= 1
            if self._readers == 0:
                self._resource_lock.release()

    def acquire_write(self):
        self._resource_lock.acquire()

    def release_write(self):
        self._resource_lock.release()

# Singleton instance
rwlock = None

def get_lock_instance():
    global rwlock
    if rwlock is None:
        rwlock = RWLock()
    return rwlock
