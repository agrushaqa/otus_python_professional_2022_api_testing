import sys

from loguru import logger


@logger.catch
def sqlite_send_request(connection, request: str, params=""):
    if connection is None:
        raise ValueError("connection is None")

    logger.debug(f"start {sys._getframe().f_code.co_name}")
    logger.debug(request)
    logger.debug(params)
    result = connection.execute(request, params)
    logger.debug(result)
    logger.debug(f"finish {sys._getframe().f_code.co_name}")
    return result
