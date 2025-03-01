#!/usr/bin/env python
import logging
import colorlog

# a theme is just a dict of strings to represent each level
THEME = {logging.CRITICAL: "CRITICAL ",
         logging.ERROR:    "ERROR ",
         logging.WARNING:  "WARNING ",
         logging.INFO:     "INFO ",
         logging.DEBUG:    "DEBUG "}


class Log:
    """
    this class holds all the logic; see the end of the script to
    see how it's instantiated in order to have the line
    "from zenlog import log" work
    """

    aliases = {
        logging.CRITICAL: ("critical", "crit", "c", "fatal"),
        logging.ERROR:    ("error", "err", "e"),
        logging.WARNING:  ("warning", "warn", "w"),
        logging.INFO:     ("info", "inf", "nfo", "i"),
        logging.DEBUG:    ("debug", "dbg", "d")
    }

    def __init__(self, lvl=logging.DEBUG, format=None):
        self._lvl = lvl
        if not format:
            format = "  %(log_color)s%(styledname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        self.format = format
        logging.root.setLevel(self._lvl)
        self.formatter = colorlog.ColoredFormatter(self.format)
        self.stream = logging.StreamHandler()
        self.stream.setLevel(self._lvl)
        self.stream.setFormatter(self.formatter)
        self.logger = logging.getLogger('pythonConfig')
        self.logger.setLevel(self._lvl)
        self.logger.addHandler(self.stream)
        self.theme = THEME
        self.extra = {"styledname": self.theme[self._lvl]}

    # the magic happens here: we use the "extra" argument documented in
    # https://docs.python.org/2/library/logging.html#logging.Logger.debug
    # to inject new items into the logging.LogRecord objects
    # we also create our convenience methods here
    def critical(self, message, *args, **kwargs):
        for line in str(message).splitlines():
            self.logger.critical(line,
                                 extra={"styledname": self.theme[logging.CRITICAL]},
                                 *args, **kwargs)
    crit = c = fatal = critical

    def error(self, message, *args, **kwargs):
        for line in str(message).splitlines():
            self.logger.error(line,
                              extra={"styledname": self.theme[logging.ERROR]},
                              *args, **kwargs)
    err = e = error

    def warn(self, message, *args, **kwargs):
        for line in str(message).splitlines():
            self.logger.warn(line,
                             extra={"styledname": self.theme[logging.WARNING]},
                             *args, **kwargs)
    warning = w = warn

    def info(self, message, *args, **kwargs):
        for line in str(message).splitlines():
            self.logger.info(line,
                             extra={"styledname": self.theme[logging.INFO]},
                             *args, **kwargs)
    inf = nfo = i = info

    def debug(self, message, *args, **kwargs):
        for line in str(message).splitlines():
            self.logger.debug(line,
                              extra={"styledname": self.theme[logging.DEBUG]},
                              *args, **kwargs)
    dbg = d = debug

    # other convenience functions to set the global logging level
    def _parse_level(self, lvl):
        for log_level in self.aliases:
            if lvl == log_level or lvl in self.aliases[log_level]:
                return log_level
        raise TypeError("Unrecognized logging level: %s" % lvl)

    def level(self, lvl=None):
        '''Get or set the logging level.'''
        if not lvl:
            return self._lvl
        self._lvl = self._parse_level(lvl)
        self.stream.setLevel(self._lvl)
        logging.root.setLevel(self._lvl)

log = Log()
