from sqlalchemy import create_engine, Column, Integer, String, Boolean, MetaData, Float, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship, declarative_base
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

db_path = config['database']['db_path']
db_path = os.path.expandvars(db_path)

if not db_path:
    raise ValueError("DATABASE_PATH environment variable is not set")

engine = create_engine(f'sqlite:///{db_path}', echo=False)
Base = declarative_base()

class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True, nullable=False)
        email = Column(String, unique=True, nullable=False)
        password = Column(String, nullable=False)
        vtoken = Column(String)
        verifiedEmail = Column(Integer, default=0)
        
        profile = relationship('Profile', uselist =False, back_populates='user') 
        matches = relationship('Match', foreign_keys='Match.user_id')

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    dob = Column(Date)
    gender = Column(String)
    interests = Column(JSON)
    career_interest = Column(String)
    education_level = Column(String)
    major = Column(String)

    user = relationship('User', back_populates='profile')


class Match(Base):
    __tablename__ = 'matches'
    match_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    matched_user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    compatibility_score = Column(Float)
    confirmed = Column(Boolean)


if not os.path.exists(db_path):

    print("DATABASE NOT CREATED. CREATING NOW...") 
    Base.metadata.create_all(engine)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if 'users' in metadata.tables and 'matches' in metadata.tables and 'profiles' in metadata.tables:
        print("SUCCESS")
    else:
        print('FAILURE')
else:
    print("DATABASE INITALIZED")