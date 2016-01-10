import sqlalchemy

import os
__module_path = os.path.dirname(__file__)

engine = sqlalchemy.create_engine('sqlite:///{0}/morphology.db'.format(__module_path), echo=False)

from .helpers import handle_special_chars, filter_chars
from .words.helpers import *
from .words.affixual import AffixualAdjunct
from .words.aspectual import AspectualAdjunct
from .words.bias import BiasAdjunct
from .words.formative import Formative
from .words.personal import PersonalAdjunct
from .words.verbal import VerbalAdjunct

def fromString(word):
	word = filter_chars(handle_special_chars(word.lower()))
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