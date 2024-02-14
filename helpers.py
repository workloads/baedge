""" application helpers """

import logging as log


def log_debug(identifier, message):
    """
    Log a debug-level item containing an identifier and a message

    Parameters:
        identifier (string):      A function or route identifier.
        message (string or dict): A string or dict of the debug message.

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
      identifier (string): A function or route identifier.
      message (string):    A string of the error message.

    Returns:
      bool: Boolean True
    """

    log.error("[%s] %s", identifier, message)

    return True


def log_exception(identifier, exception):
    """
    Log an exception-level item containing an identifier and an exception

    Parameters:
        identifier (string):   A function or route identifier.
        exception (exception): An exception of the error.

    Returns:
        bool: Boolean True
    """

    log.error("[%s] exception occurred", identifier)
    log.exception(exception)

    return True
