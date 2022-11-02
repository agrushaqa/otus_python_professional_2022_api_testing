import time

from loguru import logger


def repeat(command, number_of_repeat, timeout, *args, **kwargs):
    result = None
    for i in range(number_of_repeat):
        try:
            result = command(*args, **kwargs)
            logger.info(f"attempt № {i}. command executed successfully")
            return result
        except Exception:
            logger.exception("attempt № {i}. exception")
            time.sleep(timeout)
    return result
