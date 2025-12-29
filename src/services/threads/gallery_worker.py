from concurrent.futures import ThreadPoolExecutor

# Singleton instance
_executor = None

def get_gallery_worker_instance():
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=1)
    return _executor