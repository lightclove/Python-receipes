# -*- coding: utf-8 -*-
from configparser import ConfigParser

import psycopg2

import logging
import time


from psycopg2._psycopg import InternalError

#################################################
configParser = ConfigParser()
configFilePath = r'Snmp_Handler.conf'
configParser.read(configFilePath)
##########################################
# Config parser parameters
database = configParser.get('db', 'database')
host = configParser.get('db', 'host')
user = configParser.get('db', 'user')
password = configParser.get('db', 'password')
sslmode = configParser.get('db', 'sslmode')
# linking unified logging class and connected it to the database log writer (Db handler)
import Logger

# logger = configParser.get('log', 'logger')
# pathTolog = configParser.get('log', 'pathTolog')

logger = Logger.Logger.initLogging(
    "LogDB",
    "LogDB.log"
)
#Logging handler for PostgreSQL
class psqlHandler(logging.Handler):

    initial_sql = """CREATE TABLE IF NOT EXISTS log(
                        Created text,
                        Name text,
                        LogLevel int,
                        LogLevelName text,
                        Message text,
                        Module text,
                        FuncName text,
                        LineNo int,
                        Exception text,
                        Process int,
                        Thread text,
                        ThreadName text
                   )"""
    from datetime import datetime as dt
    insertion_sql = """INSERT INTO log(
                            created,
                            Name,
                            LogLevel,
                            LogLevelName,
                            Message,
                            Module,
                            FuncName,
                            LineNo,
                            Exception,
                            Process,
                            Thread,
                            ThreadName)
                            VALUES(
                            to_timestamp(%(created)s),
                            %(name)s,
                            %(levelno)s,
                            %(levelname)s,
                            %(message)s,
                            %(module)s,
                            %(funcName)s,
                            %(lineno)s,
                            %(exc_text)s,
                            %(process)s,
                            %(thread)s,
                            %(threadName)s
                    );"""

    def connect(self):
        try:
            self.__connect = psycopg2.connect(
                database=self.__database,
                host = self.__host,
                user = self.__user,
                password = self.__password,
                sslmode="disable")

            return True
        except:
            return False

    def __init__(self, params):

        if not params:
            raise Exception ("No database where to log ☻")

        self.__database = params['database']
        self.__host = params['host']
        self.__user = params['user']
        self.__password = params['password']

        self.__connect = None

        if not self.connect():
            raise Exception ("Database connection error, no logging ☻")

        logging.Handler.__init__(self)

        self.__connect.cursor().execute(psqlHandler.initial_sql)
        self.__connect.commit()
        self.__connect.cursor().close()

    def emit(self, record):

        # Use default formatting:
        self.format(record)

        if record.exc_info:
            #record.exc_text = logging.defaultFormatter.formatException(record.exc_info)
            record.exc_text = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

            #formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
            #fh.setFormatter(formatter)
        else:
            record.exc_text = ""

        # Insert log record:
        try:
            #cur =  self.__connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur = self.__connect.cursor()
        except:
            self.connect()
            cur = self.__connect.cursor()
        try:
            cur.execute(psqlHandler.insertion_sql, record.__dict__)
            #cur.execute(psqlHandler.insertion_sql, record.__dict__)
        except InternalError as ie:
            print(str(ie))

        self.__connect.commit()
        self.__connect.cursor().close()

if __name__ == "__main__":

    myh = psqlHandler({''
                       'host':"localhost",
                       'user':"postgres",
                       'password':"5",
                       'database':"postgres"})



    l = logging.getLogger("Snmp_Handler")
    l.setLevel(logging.DEBUG)
    l.addHandler(myh)
    l.info("Table was created...")
    print("Table was created...")

    # for i in range(1):
    #     # l.info("log%i"%i)
    #
    #     l.info("log%i"%i)
    #     l.debug("log%i"%i)
    #     l.error("log%i"%i)
    #     l.fatal("log%i"%i)
'''
from sqlalchemy import Column
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True) # auto incrementing
    level = Column(String) # info, debug, or error?
    logger = Column(String) # the name of the logger. (e.g. myapp.views)
    #trace = Column(String) # the full traceback printout
    msg = Column(String) # any custom log you may have included
    created_at = Column(DateTime, default=func.now()) # the current timestamp

    def __init__(self, logger=None, level=None, msg=None):
        self.logger = logger
        self.level = level
        #self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])
    
    # id bigint NOT NULL DEFAULT nextval('log_id_seq'::regclass),
    # log_level integer NOT NULL,
    # log_levelname character(32),
    # log_ character(2048) NOT NULL,
    # created_at timestamp with time zone NOT NULL,
    # created_by character(32) NOT NULL,
'''