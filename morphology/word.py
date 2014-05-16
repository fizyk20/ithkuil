import abc
from .helpers import *
from .data import *
from morphology import session

def split(s):
	if not s:
		return []
	elif s[0] in tones:
		return [s[0]] + split(s[1:])
	elif s[0] in consonants_s + ['’', 'ʰ', '-']:
		part = ''
		while s and s[0] in consonants_s + ['’', 'ʰ', '-']:
			part += s[0]
			s = s[1:]
		return [part] + split(s)
	elif s[0] in vowels + ['’']:
		part = ''
		while s and s[0] in vowels + ['’']:
			part += s[0]
			s = s[1:]
		return [part] + split(s)
	raise Exception('Something went terribly wrong')
	
def isPersonalAdjunct(parts):
	count_consonants = 0
	for p in parts:
		if p[0] not in vowels:
			count_consonants += 1
	if count_consonants == 1 and parts[-1][0] in vowels:
		return True
	if parts[-1][0] in vowels:
		if parts[-2] in ('w','y','h','hw'):
			return True
	else:
		if '’' in parts[-2] and parts[-3] in ('w','y','h','hw'):
			return True
	return False

def isAffixualAdjunct(parts):
	if len(parts) != 2:
		return False
	if parts[0][0] not in vowels or parts[1][0] in vowels:
		return False
	return True

def isAspectualAdjunct(parts):
	if len(parts) != 1:
		return False
	if parts[0][0] not in vowels:
		return False
	return True
	
def isBiasAdjunct(parts):
	if len(parts) != 1:
		return False
	if parts[0][0] in vowels:
		return False
	return True

class Word(metaclass=abc.ABCMeta):
	
	wordType = None
	
	def __init__(self, word):
		self.word = word
		self.parts = split(word)
		self.name = self.wordType.name
	
	@staticmethod
	def fromString(word):
		parts = split(word)
		if isPersonalAdjunct(parts):
			return PersonalAdjunct(word)
		elif isAffixualAdjunct(parts):
			return AffixualAdjunct(word)
		elif isAspectualAdjunct(parts):
			return AspectualAdjunct(word)
		elif isBiasAdjunct(parts):
			return BiasAdjunct(word)
		else:
			return Formative(word)
	
	@abc.abstractmethod
	def describe(self):
		pass
	

class Formative(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Formative').first()
	
	def describe(self):
		return 'Formative'
	

class PersonalAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
	
	def describe(self):
		return 'Personal adjunct'
	

class AffixualAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Affixual adjunct').first()
	
	def describe(self):
		return 'Affixual adjunct'
	

class AspectualAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Aspectual adjunct').first()
	
	def describe(self):
		return 'Aspectual adjunct'
	

class BiasAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Bias adjunct').first()
	
	def describe(self):
		return 'Bias adjunct'
	