import sqlalchemy
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///morphology/morphology.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

from .data import *
from .word import *