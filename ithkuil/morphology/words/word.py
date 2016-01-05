import abc
from .helpers import split
from ..data import ithSlot, ithMorpheme
from .. import Session
from ..exceptions import IthkuilException, AnalysisException

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
			try:
				self.analyze()
			except IthkuilException:
				raise
			except:
				raise IthkuilException('Invalid Ithkuil word: %s' % self.word)
		return self._slots
	
	@property
	def tone(self):
		if '[tone]' in self.slots:
			return self.slots['[tone]']
		return '\\'
	
	def morpheme(self, slot, content, wordType=None):
		if not wordType:
			wordType = self.wordType
		session = Session()
		slotObj = session.query(ithSlot).filter(ithSlot.word_type_id == wordType.id).filter(ithSlot.name == slot).all()
		if len(slotObj) != 1:
			return content
		slotObj = slotObj[0]
		morph = session.query(ithMorpheme).filter(ithMorpheme.slot_id == slotObj.id).filter(ithMorpheme.content == content).all()
		if len(morph) > 1:
			return None
		if len(morph) == 0:
			if wordType.name == 'Formative' and (slot == 'Cr' or slot == 'Cx'):
				return content
			else:
				raise AnalysisException('Invalid content for slot %s of word type %s: %s' % (slot, wordType.name, content))
		return morph[0]
	