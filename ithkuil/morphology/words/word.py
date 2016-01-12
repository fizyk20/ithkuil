import abc
from ithkuil.morphology.database import ithSlot, ithMorphemeSlot, ithAtom, Session
from ..exceptions import AnalysisException

class Word(metaclass=abc.ABCMeta):

	wordType = None
	_slots = None

	def __init__(self, word, slots):
		self.word = word
		self._slots = slots
		self.analyze()

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
		return self._slots

	@property
	def tone(self):
		if '[tone]' in self.slots:
			return self.slots['[tone]']
		return '\\'

	@property
	def stress(self):
		if '[stress]' in self.slots:
			return self.slots['[stress]']
		return -2

	def morpheme(self, slot, content):
		session = Session()
		slotObj = session.query(ithSlot).filter(ithSlot.wordtype == self.wordType).filter(ithSlot.name == slot).all()
		if len(slotObj) != 1:
			return content
		slotObj = slotObj[0]
		morph = session.query(ithMorphemeSlot).filter(ithMorphemeSlot.slot_id == slotObj.id).filter(ithMorphemeSlot.morpheme.has(morpheme = content)).all()
		if len(morph) > 1:
			return None
		if len(morph) == 0:
			raise AnalysisException('Invalid content for slot %s of word type %s: %s' % (slot, self.wordType.name, content))
		return morph[0]

	def atom(self, *morphemes):
		if len(morphemes) == 1 and isinstance(morphemes[0], str):
			return morphemes[0]
		session = Session()
		query = session.query(ithAtom)
		for morpheme in morphemes:
			query = query.filter(ithAtom.morpheme_slots.contains(morpheme))
		result = query.all()
		if len(result) == 0:
			return None
		elif len(result) == 1:
			return result[0]
		else:
			raise AnalysisException('Non-unique atom defined by morphemes: %s' %
				', '.join(map(lambda x: '%s=%s' % (x.slot.name, x.morpheme.morpheme), morphemes)))
