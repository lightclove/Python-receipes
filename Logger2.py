# -*- coding: utf-8 -*-
import logging

class Logger:
    ''' Handles logging of debugging and error messages. '''

    @staticmethod
    def initLogging(loggerName, pathToLogFileName):
        # START LOGGING SECTION
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)
        # create the logging file handler
        # logging.basicConfig(filename="Snmp_Request.log", level=logging.DEBUG)
        fh = logging.FileHandler(pathToLogFileName)
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        fh.setFormatter(formatter)
        # # add handler to logger object
        logger.addHandler(fh)
        return logger
        # END LOGGING SECTION
        ###

########################################################################################################################

    DEBUG = 5
    INFO = 4
    WARN = 3
    ERROR = 2
    FATAL = 1
    _level = DEBUG

    def __init__(self):
        Logger._level = Logger.DEBUG

    @classmethod
    def isLevel(cls, level):
        return cls._level >= level

    @classmethod
    def debug(cls, message):
        if cls.isLevel(Logger.DEBUG):
            print("DEBUG:  " + message)

    @classmethod
    def info(cls, message):
        if cls.isLevel(Logger.INFO):
            print("INFO :  " + message)

    @classmethod
    def warn(cls, message):
        if cls.isLevel(Logger.WARN):
            print("WARN :  " + message)

    @classmethod
    def error(cls, message):
        if cls.isLevel(Logger.ERROR):
            print("ERROR:  " + message)

    @classmethod
    def fatal(cls, message):
        if cls.isLevel(Logger.FATAL):
            print("FATAL:  " + message)

myh = psqlHandler({''
                    'host': host,
                    'user': user,
                    'password': password,
                    'database': database})
