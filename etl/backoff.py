from functools import wraps
import time
from logger import logger


def backoff(start_sleep_time, factor, border_sleep_time):
    """
        Decorator implementing exponential backoff strategy for handling exceptions.

        :param start_sleep_time (float, optional): Initial sleep time in seconds. Defaults to 0.1.
        :param factor (int, optional): Exponential factor. Defaults to 2.
        :param border_sleep_time (float, optional): Maximum sleep time in seconds. Defaults to 10.

        :return: The decorated function with backoff behavior.
        """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(e)
                    time_sleep = start_sleep_time * (factor ** n)
                    if time_sleep > border_sleep_time:
                        time_sleep = border_sleep_time
                    time.sleep(time_sleep)
                    n += 1
                    if time_sleep == border_sleep_time:
                        logger.error(f'the function {func.__name__} will not be executed due to an error:{str(e)}')
        return inner

    return func_wrapper
