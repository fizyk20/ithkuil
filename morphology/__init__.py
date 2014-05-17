import sqlalchemy
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///morphology/morphology.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

from .data import *
from .word import *
from .formative import Formative

def fromString(word):
	parts = split(word)
	if isVerbalAdjunct(parts):
		return VerbalAdjunct(word)
	elif isPersonalAdjunct(parts):
		return PersonalAdjunct(word)
	elif isAffixualAdjunct(parts):
		return AffixualAdjunct(word)
	elif isAspectualAdjunct(parts):
		return AspectualAdjunct(word)
	elif isBiasAdjunct(parts):
		return BiasAdjunct(word)
	else:
		return Formative(word)