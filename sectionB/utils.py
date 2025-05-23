import time
import functools

def timed_query(repeats=5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            total_time = 0.0
            for i in range(repeats):
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                total_time += elapsed
                print(f"Run {i+1}/{repeats}: {elapsed:.4f} seconds")
            avg_time = total_time / repeats
            print(f"Average execution time for {func.__name__} over {repeats} runs: {avg_time:.4f} seconds")
            return result 
        return wrapper
    return decorator

