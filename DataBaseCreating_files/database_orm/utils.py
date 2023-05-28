from sqlalchemy import create_engine
from sqlalchemy import URL
from core import Club

def get_engine(user="root", password="", host="localhost", db = None, *args, **kwargs) :
    url_object = URL.create(
        "mysql+mysqlconnector",
        username=user,
        password=password,  # plain (unescaped) text
        host=host,
        database=db
    )

    engine = create_engine(url_object)

    return engine
