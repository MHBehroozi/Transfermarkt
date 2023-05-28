from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL

from sqlalchemy import String, Integer, Column, ForeignKey, Float, Date, PrimaryKeyConstraint
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
    league_name = Column(String(30))
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
    club_id = Column(Integer, ForeignKey('club.id'))
    win_year = Column(Integer)
    # nation = Column(String(30))

    __table_args__ = (
            PrimaryKeyConstraint(club_id, award_id, win_year),
        )
    def __repr__(self) -> str:
        return f"Award_winners(award_id= \n{self.award_id} \n cup_id= {self.cup_id}\n win_year= {self.win_year} \n nation= {self.nation})"

# Coach name,Appointed Date,id

class Coach(Base):
    __tablename__ = "coach"

    # declare columns
    # id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    club_id = Column(Integer, ForeignKey('club.id'))
    coach_name = Column(String(60)
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
    club_id = Column(Integer, ForeignKey('club.id'))
    stadium_name = Column(String(60))

    __table_args__ = (
            PrimaryKeyConstraint(club_id, stadium_name),
        )
    # club_id = relationship('Club', foreign_keys='club.id')

    def __repr__(self) -> str:
        return f"Coach( club_id= {self.club_id}\n coach_name= {self.coach_name}\n appointed_date= {self.appointed_date} )"



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
