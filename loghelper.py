import sys
import logging


def logHelper(fileName, logLevel=logging.INFO, useConsole=True):
    """
    Simple Logging Helper. Retuens logger reference.
    Paramsmeters:
    fileName: Filename, may include full path, or will open a file in default folder
    logLevel: Pass logging.INFO, logging.DEBUG or other enums for logging level
    useConsole: If Ture, will also dump log to console
    """

    # init logging
    log = logging.getLogger()
    log.setLevel(logLevel)
    logFormatter = logging.Formatter(fmt='%(asctime)s [%(levelname)8s] %(message)s',
                                     datefmt="%y-%m-%d %h:%m:%s")

    # file handler
    fileOut = logging.FileHandler(fileName)
    fileOut.setFormatter(logFormatter)
    log.addHandler(fileOut)

    # console handler
    if useConsole:
        consoleOut = logging.StreamHandler(sys.stdout)
        consoleOut.setFormatter(logFormatter)
        log.addHandler(consoleOut)

    # return reference
    return log
