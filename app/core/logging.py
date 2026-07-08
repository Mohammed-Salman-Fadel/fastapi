import logging

def setup_logging():
    logging.basicConfig(filename="addresses.log", 
                    level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')
