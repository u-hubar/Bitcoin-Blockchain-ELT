import functools
import time


def exponential_backoff(logger, retries=3, backoff=1, delay=0.1):
    """
    Retry function decorator using exponential backoff algorithm
        logger              - logging object
        retries(R)          - how many times function should try to execute
        backoff(B)          - exponential waiting time base number B^r + D
        delay(D)            - exponential waiting time static number B^r + D
    """
    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            for r in range(retries + 1):
                result = f(*args, **kwargs)

                if result is not None:
                    return result
                else:
                    logger.debug(
                        f"({r}/{retries}) Failed to execute {f.__name__}."
                    )
                    time.sleep((backoff ** r) + delay)

        return inner
    return wrap
