from functools import wraps
import time
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', filemode='w')


def log_exec_time(f):
    """
    A decorator for logging function execution time, calls information
    and exceptions info, if any occurs.

    :param f: Function to be decorated.
    :return: Decorated function.
    """
    @wraps(f)
    def time_count_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = f(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            logging.info(f'fuction {f.__name__} executed in {total_time:.2} seconds')
            logging.info(f"Function {f.__name__} called with args: {args} and kwargs: {kwargs}")
            return result
        except Exception as e:
            logging.error(f'Function {f.__name__} raised exception {type(e).__name__}: {str(e)}')
            raise e
    return time_count_wrapper


