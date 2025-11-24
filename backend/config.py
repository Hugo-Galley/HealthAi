import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from EasyWorkEnv import Config

configuration = Config("variables.json")


def config_database():
    user = configuration.Bdd.User
    password = configuration.Bdd.Password
    host = configuration.Bdd.Host
    port = configuration.Bdd.Port
    database = configuration.Bdd.DataBase

    connection = pymysql.connect(
        host=host, user=user, password=password, database=database, port=port
    )
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}`")
    connection.close()

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    return db


db = config_database()
