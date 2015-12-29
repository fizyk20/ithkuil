import abc
from .helpers import *
from .data import *
from .exceptions import *
from . import Session

def split(s):
	if not isinstance(s, str):
		raise TypeError('Word should be a string')
	s = s.lower()
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
	raise InvalidCharacter(s[0])

def isVerbalAdjunct(parts):
	if parts[-1][0] in vowels:
		if '-' in parts[-2]:
			return True
	else:
		if '-' in parts[-1]:
			return True
		if len(parts) > 2 and '-' in parts[-3]:
			return True
	return False
	
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
	_slots = None
	
	def __init__(self, word):
		self.word = word
		self.parts = split(word)
		self.type = self.wordType.name
		
	def __getattr__(self, attr):
		if self.slots and attr in self.slots:
			return self.slots[attr]
		raise AttributeError()
	
	@abc.abstractmethod
	def abbreviatedDescription(self):
		pass
	
	@abc.abstractmethod
	def fullDescription(self):
		pass
	
	@abc.abstractmethod
	def analyze(self):
		pass
	
	@property
	def slots(self):
		if not self._slots:
			self.analyze()
		return self._slots
	
	@property
	def tone(self):
		if '[tone]' in self.slots:
			return self.slots['[tone]']
		return '\\'
	
	def morpheme(self, slot, content):
		session = Session()
		slotObj = session.query(ithSlot).filter(ithSlot.word_type_id == self.wordType.id).filter(ithSlot.name == slot).all()
		if len(slotObj) != 1:
			return content
		slotObj = slotObj[0]
		morph = session.query(ithMorpheme).filter(ithMorpheme.slot_id == slotObj.id).filter(ithMorpheme.content == content).all()
		if len(morph) > 1:
			return None
		if len(morph) == 0:
			return content
		return morph[0]
	

class VerbalAdjunct(Word):
	
	wordType = Session().query(ithWordType).filter(ithWordType.name == 'Verbal adjunct').first()
	
	def analyze(self):
		parts = self.parts[:]
		self._slots = {}
	
		if len(parts)>2 and parts[-2][-1] == '’':
			parts[-2] = parts[-2][:-1]
			self._slots['G'] = parts[-1]
			parts = parts[:-1]
		
		if parts[-1][0] in vowels:
			self._slots['F'] = parts[-1]
			parts = parts[:-1]
			
		if parts[0] in tones:
			self._slots['H'] = parts[0]
			parts = parts[1:]
			
		self._slots['E'] = parts[-1]
		if len(parts) > 1:
			self._slots['D'] = parts[-2]
		if len(parts) > 2:
			self._slots['C'] = parts[-3]
		if len(parts) > 3:
			self._slots['B'] = parts[-4]
		if len(parts) > 4:
			self._slots['A'] = parts[-5]
	
	def abbreviatedDescription(self):
		return 'Verbal adjunct'
	
	def fullDescription(self):
		return {'type': 'Verbal adjunct', 'categories': []}
	

class PersonalAdjunct(Word):
	
	wordType = Session().query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
	
	def analyze(self):
		parts = self.parts[:]
		self._slots = {}
	
		if parts[0] in tones:
			self._slots['[tone]'] = parts[0]
			parts = parts[1:]
			
		if parts[-1][0] not in vowels:
			self._slots['bias'] = parts[-1]
			parts[-2] = parts[-2][:-1]
			parts = parts[:-1]
			
		if parts[-2] in ('w', 'y', 'h', 'hw'):
			self._slots['Cz'] = parts[-2]
			self._slots['Vz'] = parts[-1]
			if parts[-3][-1] == '’':
				parts[-3] = parts[-3][:-1]
				self._slots['Cz'] = '’' + self._slots['Cz']
			parts = parts[:-2]
			
		self._slots['C1'] = parts[-2]
		self._slots['V1'] = parts[-1]
		parts = parts[:-2]
		
		if (len(self._slots['C1']) == 1 and self._slots['C1'] not in ('g', 'd', 'j', 'ż', 'c', 'b')) or self._slots['C1'] == 'xh':
			#single-referent
			self._slots['CsVs'] = []
			if len(parts) == 1:
				self._slots['V2'] = parts[0]
			else:
				while parts:
					self._slots['CsVs'].append((parts[-1], parts[-2]))
					parts = parts[:-2]
		else:
			#dual-referent
			self._slots['Ck'] = self._slots['C1']
			del self._slots['C1']
			
			self._slots['V2'] = parts[-1]
			parts = parts[:-1]
			if parts:
				self._slots['C2'] = parts[-1]
				parts = parts[:-1]
			if parts:
				self._slots['Vw'] = parts[-1]
		
	def abbreviatedDescription(self):
		return 'Personal adjunct'
		
	def fullDescription(self):
		return {'type': 'Personal adjunct', 'categories': []}
	

class AffixualAdjunct(Word):
	
	wordType = Session().query(ithWordType).filter(ithWordType.name == 'Affixual adjunct').first()
	
	def analyze(self):
		self._slots = {1: (self.parts[0], self.parts[1])}
		
	def abbreviatedDescription(self):
		return 'Affixual adjunct'
		
	def fullDescription(self):
		return {'type': 'Affixual adjunct', 'categories': []}
	

class AspectualAdjunct(Word):
	
	wordType = Session().query(ithWordType).filter(ithWordType.name == 'Aspectual adjunct').first()
	
	def analyze(self):
		self._slots = {1: self.parts[0]}
		
	def abbreviatedDescription(self):
		return 'Aspectual adjunct'
		
	def fullDescription(self):
		return {'type': 'Aspectual adjunct', 'categories': []}
	

class BiasAdjunct(Word):
	
	wordType = Session().query(ithWordType).filter(ithWordType.name == 'Bias adjunct').first()
	
	def analyze(self):
		self._slots = {1: self.parts[0]}
		
	def abbreviatedDescription(self):
		return 'Bias adjunct'
		
	def fullDescription(self):
		return {'type': 'Bias adjunct', 'categories': []}
	