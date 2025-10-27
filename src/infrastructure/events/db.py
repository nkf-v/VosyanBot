from dataclasses import dataclass
from os import getenv, path
from dotenv import load_dotenv

from playhouse.pool import PooledMySQLDatabase

@dataclass
class DBCredential:
    db_host: str
    db_name: str
    username: str
    password: str
    charset: str
    collation: str
    max_connections: int
    stale_timeout: int

class DBCredentialProvider:
    def load(self):
        load_dotenv(path.abspath('.env'))
        return self

    def provide(self) -> DBCredential:
        return DBCredential(
            db_host= getenv('DB_HOST'),
            db_name=getenv('DB_NAME'),
            username= getenv('DB_USER'),
            password=getenv('DB_PASSWORD'),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            max_connections=4,
            stale_timeout=15,
        )

class DBConnectFactory:
    __connect = None
    __cred_provider: DBCredentialProvider

    def __init__(self, cred_provider: DBCredentialProvider):
        self.__cred_provider = cred_provider

    def create(self):
        if DBConnectFactory.__connect is None:
            creds = self.__cred_provider.load().provide()

            DBConnectFactory.__connect = PooledMySQLDatabase(
                creds.db_name,
                user=creds.username,
                password=creds.password,
                host=creds.db_host,
                charset=creds.charset,
                collation=creds.collation,
                max_connections=creds.max_connections,
                stale_timeout=creds.stale_timeout,
            )

        return DBConnectFactory.__connect
