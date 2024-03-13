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


def generate_relative_coordinates(height, width, offset, object_size):
    """
    Log an exception-level item containing an identifier and an exception

    Parameters:
        height (int):      Height of the eInk screen.
        width (int):       Width of the eInk screen.
        offset (int):      Offset of the object.
        object_size (int): Size of the object.

    Returns:
        bool: Boolean True
    """

    longer_side = max(height, width)
    shorter_side = min(height, width)

    log_debug('generate_relative_coordinates', f'longer_side: {longer_side}, shorter_side: {shorter_side}')

    x = 0
    y = 0

    # if offset is negative, place object relative to bottom right corner
    if offset < 0:
        # calculate position of object by substracting offset and object size from bottom right coordinates
        # bottom right coordinates are the edge of the (height x width)
        x = int(longer_side - (abs(offset) * longer_side) - object_size[0])
        y = int(shorter_side - (abs(offset) * shorter_side) - object_size[1])

    else:
        # offset is positive, place object relative to upper left corner
        x = int(offset * longer_side)
        y = int(offset * shorter_side)

    print(x, y)
    return x, y


def format_url_map(url_map, hidden_routes, visible_methods, visible_prefix):
    """
    Format a (Flask) URL Map to meet certain conditions

    Parameters:
        url_map (object):        Object of Flask URL Maps
        hidden_routes (list):    List of Routes that should be hidden (omitted)
        visible_methods (list):  List of (HTTP) Methods that should be visible
        visible_prefix (string): Prefix of the visible routes

    Returns:
        object: Object containing formatted routes
    """

    routes = {
        method: [] for method in visible_methods
    }

    # iterate over all received URLs
    for route in url_map:
        # only consider rules that start with `visible_prefix`
        if str(route).startswith(visible_prefix):

            methods = [
              method for method in route.methods if method in visible_methods
            ]

            for method in methods:
                log_debug('format_url_map', f'route: {route}, method: {method}')
                routes[method].append(str(route))

    print(routes)
    return routes
