from .word import Word
from .formative import Formative
from ..data import ithWordType
from .. import Session  

class AffixualAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Affixual adjunct').first()
    
    def analyze(self):
        self._slots = {1: (self.parts[0], self.parts[1])}
        
    def abbreviatedDescription(self):
        deg = self.morpheme('VxC', self.slots[1][0], Formative.wordType).values[0].code
        suf = self.morpheme('VxC', self.slots[1][1], Formative.wordType).values[0].code
        return '%s_%s' % (suf, deg)
        
    def fullDescription(self):
        deg = self.morpheme('VxC', self.slots[1][0], Formative.wordType).values[0]
        suf = self.morpheme('VxC', self.slots[1][1], Formative.wordType).values[0]
        return { 
            'type': 'Affixual adjunct', 
            'categories': ['Type', 'Degree'],
            'Type': { 'code': suf.code, 'name': suf.code },
            'Degree': { 'name': deg.name }
        }