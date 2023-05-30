from sqlalchemy import create_engine
from sqlalchemy import URL
from core import Club, Player
from sqlalchemy.orm import sessionmaker

import pandas as pd


def get_engine(user="root", password="", host="localhost", db=None, *args, **kwargs):
    url_object = URL.create(
        "mysql+mysqlconnector",
        username=user,
        password=password,  # plain (unescaped) text
        host=host,
        database=db
    )

    engine = create_engine(url_object)

    return engine


def complete_player_data(db=None, player_id=None, birth_date=None, height=None, main_position=None, agent=None, name=None, foot=None):

    try:

        Session = sessionmaker(bind=get_engine(db=db))
        session = Session()

        instance =  dict()
        if not pd.isna(birth_date) :
            instance['birth_date'] = birth_date
        if not pd.isna(height) :
            instance['height'] = height
        if not pd.isna(main_position) :
            instance['main_position'] = main_position
        if not pd.isna(agent) :
            instance['agent'] = agent
        if not pd.isna(name) :
            instance['name'] = name
        if not pd.isna(foot) :
            instance['foot'] = foot
        
        

        qry_object = session.query(Player).where(Player.id == newPlayer.id)
        if qry_object.first() is None:
            print("not fount", newPlayer)
            newPlayer = Player(
                id = player_id,
                    birth_date = birth_date,
                    height = height,
                    main_position = main_position,
                    name = name,
                    agent = agent,
                    foot = foot)
            session.add(newPlayer)
        else:
            print("update  player")
            session.query(Player).filter(Player.id == player_id).update(instance)
        session.commit()
        session.close()

        return True

    except Exception as exc:
        print(f"Error updating data from CSV: {str(exc)}")
        return False
