""" application helpers """

import logging as log


def log_info(identifier, message):
    """
    Log an info-level item containing an identifier and a message

    Parameters:
      identifier (string):      Function or route identifier.
      message (string or dict): String or Dict of info-level message.

    Returns:
      bool: Boolean True
    """

    # if `message` is a dict, print the individual keys and values
    if isinstance(message, dict):
        log.info("[%s] \n%s\n", identifier, ", ".join(f"\n{key}: {value}" for key, value in message.items()))
    else:
        log.info("[%s] %s", identifier, message)

    return True


def log_debug(identifier, message):
    """
    Log a debug-level item containing an identifier and a message

    Parameters:
        identifier (string):      Function or route identifier.
        message (string or dict): String or Dict of debug-level message.

    Returns:
        bool: Boolean True
    """

    # if `message` is a dict, print the individual keys and values
    if isinstance(message, dict):
        log.debug("[%s] \n%s\n", identifier, ", ".join(f"\n{key}: {value}" for key, value in message.items()))
    else:
        log.debug("[%s] %s", identifier, message)

    return True


def log_error(identifier, message):
    """
    Log an error-level item containing an identifier and a message

    Parameters:
      identifier (string):      Function or route identifier.
      message (string or dict): String of error-level message.

    Returns:
      bool: Boolean True
    """

    log.error("[%s] %s", identifier, message)

    return True


def log_exception(identifier, exception):
    """
    Log an exception-level item containing an identifier and an exception

    Parameters:
        identifier (string):   Function or route identifier.
        exception (exception): Exception.

    Returns:
        bool: Boolean True
    """

    log.error("[%s] exception occurred", identifier)
    log.exception(exception)

    return True
