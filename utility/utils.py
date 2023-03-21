from functools import wraps
import time
def time_count(f):
    """
    Time-measuring decorator
    :param f: function
    :return: str
    """
    @wraps(f)
    def time_count_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = f(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        print(f'Function {f.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return time_count_wrapper