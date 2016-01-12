from .word import Word
from ithkuil.morphology.database import ithWordType, Session
from ..helpers import vowels, tones

class PersonalAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()

    def analyze(self):
        pass

    def abbreviatedDescription(self):
        return 'Personal adjunct'

    def fullDescription(self):
        return {'type': 'Personal adjunct', 'categories': []}
