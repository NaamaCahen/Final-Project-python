import random

db_info = {'host': 'topsy.db.elephantsql.com',
           'database': 'yftjgjsj',
           'psw': 'Mspp5BdU4tpGbybssXSb3vy0MGrbA31M',
           'user': 'yftjgjsj',
           'port': '5432'}


class Config:
    SECRET_KEY = random._urandom(56)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"
