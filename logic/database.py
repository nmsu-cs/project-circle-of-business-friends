from sqlalchemy import create_engine, Column, Integer, String, MetaData, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

db_path = config['database']['db_path']
db_path = os.path.expandvars(db_path)

if not db_path:
    raise ValueError("DATABASE_PATH environment variable is not set")

engine = create_engine(f'sqlite:///{db_path}', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    interests = Column(String)
    occupation = Column(String)
    education_level = Column(String)
    major = Column(String)

class Match(Base):
    __tablename__ = 'matches'
    match_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    matched_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    compatibility_score = Column(Float)
    
    user = relationship("User", foreign_keys=[user_id])
    matched_user = relationship("User", foreign_keys=[matched_user_id])
    
Base.metadata.create_all(engine)

metadata = MetaData()
metadata.reflect(bind=engine)

if 'users' in metadata.tables and 'matches' in metadata.tables:
    print("SUCCESS")
else:
    print('FAILURE')