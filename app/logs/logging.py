import logging

def setup_logging():
    logging.basicConfig(filename="app/logs/logs.log", 
                    level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')
