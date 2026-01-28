from concurrent.futures import ThreadPoolExecutor

# Singleton instance
_executor = None

def get_action_queue_instance(max_workers=1):
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=max_workers)
    return _executor