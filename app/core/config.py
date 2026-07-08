# from pydantic_core import BaseSettings

class Config():
    app_name: str = "AddressBookApplication"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "addresses.db"
    
config = Config()

