import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

import os
__module_path = os.path.dirname(__file__)

engine = sqlalchemy.create_engine('sqlite:///{0}/morphology.db'.format(__module_path), echo=False)
Session = scoped_session(sessionmaker(bind=engine))

from .data import *
from .word import *
from .helpers import handle_special_chars
from .formative import Formative

def fromString(word):
	word = handle_special_chars(word)
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