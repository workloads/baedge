""" Baedge Application """

import logging as log


def log_debug(function, msg):
    """ create log message for debugging """

    log.debug("[%s] %s", function, msg)


def log_error(function, msg):
    """ create log message for errors """

    log.error("[%s] %s", function, msg)


def log_exception(function, exception):
    """ create log message for exceptions """

    log.error("[%s] exception occurred", function)
    log.exception(exception)
