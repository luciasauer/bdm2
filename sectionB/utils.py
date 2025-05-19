import time

def timed_query(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        query_time = time.time() - start_time
        print(f"{func.__name__} executed in {query_time:.4f} seconds")
        return result
    return wrapper
