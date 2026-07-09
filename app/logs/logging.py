import logging

# The basic logging setup that i will be using 
def setup_logging():
    logging.basicConfig(filename="app/logs/logs.log", 
                    level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')
