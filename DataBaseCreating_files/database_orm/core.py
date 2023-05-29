from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL

from sqlalchemy import String, Integer, Column, ForeignKey, Float, Date, PrimaryKeyConstraint, Enum
from sqlalchemy.orm import relationship


from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import text


class Base(DeclarativeBase):
    pass


class Club(Base):
    __tablename__ = "club"

    # declare columns
    id = Column(Integer, primary_key=True)
    club = Column(String(60))
    country = Column(String(30))

    def __repr__(self) -> str:
        return f"Club(id= \n{self.id} \n club= \n{self.club} \n country= {self.country})"

    pass

# id,Season,income,expend,overall_balance,ARRIVALS,DEPARTURES,League name,Average age of players,Total market value

class Club_stats(Base):
    __tablename__ = "club_stats"

    # declare columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer)
    season = Column(Integer)
    income = Column(Float(precision='30,2'))
    expend = Column(Float(precision='30,2'))
    overall_balance = Column(Float(precision='30,2'))
    arrivals = Column(String(30))
    departures = Column(String(30))
    league_name = Column(String(50))
    player_avg_age = Column(String(30))
    total_market_value= Column(Float(precision='30,2'))

    def __repr__(self) -> str:
        return f"Club_stats(club_id= \n{self.id}  \n season= {self.season}) \n income= {self.income})\n expend= {self.expend})\n overall_balance= {self.overall_balance})\n arrivals= {self.arrivals})\n departures= {self.departures})\n league_name= {self.league_name} \n player_avg_age= {self.player_avg_age}\n total_market_value= {self.total_market_value})"

#     pass


class Awards(Base):
    __tablename__ = "awards"

    # declare columns
    award_id = Column(String(60), primary_key=True)
    cup_name = Column(String(30))

    def __repr__(self) -> str:
        return f"Awards(award_id= \n{self.award_id} \n cup_name= {self.cup_name})"


class Award_winners(Base):
    __tablename__ = "award_winners"

    # declare columns
    award_id = Column(String(60))
    club_id = Column(Integer)
    win_year = Column(Integer)

    __table_args__ = (
            PrimaryKeyConstraint(club_id, award_id, win_year),
        )
    def __repr__(self) -> str:
        return f"Award_winners(award_id= \n{self.award_id} \n cup_id= {self.cup_id}\n win_year= {self.win_year} )"

# Coach name,Appointed Date,id

class Coach(Base):
    __tablename__ = "coach"

    # declare columns
    club_id = Column(Integer)
    coach_name = Column(String(60))
    appointed_date = Column(Date)

    # club_id = relationship('Club', foreign_keys='club.id')

    __table_args__ = (
            PrimaryKeyConstraint(club_id, coach_name, appointed_date),
        )

    def __repr__(self) -> str:
        return f"Coach( club_id= {self.club_id}\n coach_name= {self.coach_name}\n appointed_date= {self.appointed_date} )"

class Stadium(Base):
    __tablename__ = "stadium"

    # declare columns
    club_id = Column(Integer)
    stadium_name = Column(String(60))

    __table_args__ = (
            PrimaryKeyConstraint(club_id, stadium_name),
        )
    # club_id = relationship('Club', foreign_keys='club.id')

    def __repr__(self) -> str:
        return f"Coach( club_id= {self.club_id}\n coach_name= {self.coach_name}\n appointed_date= {self.appointed_date} )"

class Player(Base):
    __tablename__ = "player"

    # declare columns
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    birth_date = Column(Date)
    height = Column(Float(5))
    main_position = Column(String(50))
    foot = Column(Enum('left', 'right', 'both', name='player_foot'))
    agent = Column(String(50))

    def __repr__(self) -> str:
        return f"Player( id= {self.id}\n name= {self.name}\n birth_date= {self.birth_date} \n height= {self.height} \n main_position= {self.main_position} \n foot= {self.foot} \n agent= {self.agent} )"

class Player_statistics(Base):
    __tablename__ = "player_statistics"

    # declare columns
    #player_id,season,Competition,club full name,Squad,Appearances,PPG,Goals,Own goals,Substitutions on,Substitutions off,Yellow cards,
    # Second yellow cards,Red cards,Goals conceded,
    # Clean sheets,Minutes played,Assists,Penalty goals,Minutes per goal,club_id,club name,market_value
    player_id = Column(Integer)
    club_id = Column(Integer)
    season = Column(Integer)
    competition = Column(String(60))
    club_full_name = Column(String(20))
    squad = Column(Integer)
    appearances = Column(Integer)
    PPG = Column(Float(2))
    goals = Column(Integer)
    own_goals = Column(Integer)
    substitutions_on = Column(Integer)
    substitutions_off = Column(Integer)
    yellow_cards = Column(Integer)
    second_yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    goals_conceded = Column(Integer)
    clean_sheets = Column(Integer)
    minutes_played = Column(Float(3))
    assists = Column(Integer)
    penalty_goals = Column(Integer)
    minutes_per_goal = Column(Integer)
    club_name = Column(String(50))
    market_value = Column(Float(precision='30,2'))

    __table_args__ = (
            PrimaryKeyConstraint(club_id, player_id, season, competition),
        )

    def __repr__(self) -> str:
        return f"Player_statistics( player_id= {self.player_id}\n club_id= {self.club_id}\n season= {self.season} \n competition= {self.competition} \n squad= {self.squad} \n appearances= {self.appearances} \n PPG= {self.PPG} \n goals= {self.goals} \n own_goals= {self.own_goals} \n substitutions_on= {self.substitutions_on}\n substitutions_off= {self.substitutions_off}\n yellow_cards= {self.yellow_cards} \n second_yellow_cards= {self.second_yellow_cards} \n red_cards= {self.red_cards} \n goals_conceded= {self.goals_conceded} \n clean_sheets= {self.clean_sheets} \n minutes_played= {self.minutes_played} \n assists= {self.assists} \n penalty_goals= {self.penalty_goals} \n minutes_per_goal= {self.minutes_per_goal} \n market_value= {self.market_value} )"


class Player_transfers(Base):
    __tablename__ = "player_transfers"

    # declare columns
    # player_id,MV,Transfer_Fee,left,joined,Date,season,Loan_Fee,transfer/loan
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer)
    MV = Column(Integer)
    transfer_Fee = Column(Float(precision='10,2'))
    left = Column(Integer())
    joined = Column(String(20))
    date = Column(Date)
    season = Column(Integer)
    loan_fee = Column(Float(2))
    transfer_loan = Column(Integer)
    
   
    def __repr__(self) -> str:
        return f"Player_transfers( player_id= {self.player_id}\n MV= {self.MV}\n transfer_Fee= {self.transfer_Fee} \n left= {self.left} \n joined= {self.joined} \n date= {self.date} \n season= {self.season} \n loan_fee= {self.loan_fee} \n transfer_loan= {self.transfer_loan}  )"


DB_NAME = 'quera_project1'

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="",  # plain (unescaped) text
    host="localhost",
    database=DB_NAME
)
engine = create_engine(url_object)

with engine.connect() as conn:
    print('Check whether table exists')
    res = conn.execute(text("show tables;"))

    try:
        Base.metadata.create_all(engine)
    except Exception as error:
        print("err:", error)
