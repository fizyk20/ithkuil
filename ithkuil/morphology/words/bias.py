from .word import Word
from .formative import Formative
from ithkuil.morphology.database import ithWordType, Session

class BiasAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Bias adjunct').first()
    
    def analyze(self):
        part = self.parts[0]
        if len(part) > 1 and part[-2] == part[-1]:
            self._slots = {1: self.parts[0][:-1], 'plus': True}
        elif part == 'xxh':
            self._slots = {1: 'xh', 'plus': True}
        else:
            self._slots = {1: self.parts[0], 'plus': False}
        
    def abbreviatedDescription(self):
        return 'Bias adjunct: %s%s' % (self.morpheme('Cb', self.slots[1], Formative.wordType).values[0].code, '+' if self.slots['plus'] else '')
        
    def fullDescription(self):
        mor = self.morpheme('Cb', self.slots[1], Formative.wordType).values[0]
        return {
            'type': 'Bias adjunct',
            'categories': ['Bias'],
            'Bias': {'code': mor.code, 'name': mor.name}
        }
