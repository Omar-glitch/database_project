from pydantic import BaseSettings
from os import environ

class Settings(BaseSettings):
    HOST : str = environ['HOST']
    PORT : int = environ['PORT']
    DEBUG : bool = environ['DEBUG']
    POSTGRES_USER : str = environ['POSTGRES_USER']
    POSTGRES_PASSWORD : str = environ['POSTGRES_PASSWORD']
    POSTGRES_HOST : str = environ['POSTGRES_HOST']
    POSTGRES_DATABASE : str = environ['POSTGRES_DATABASE']
    POSTGRES_SCHEMA : str = environ['POSTGRES_SCHEMA']
    POSTGRES_PORT : int = environ['POSTGRES_PORT']
