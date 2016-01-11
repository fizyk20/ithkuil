from .word import Word
from .formative import Formative
from ..data import ithWordType, Session

class AffixualAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Affixual adjunct').first()
    
    def analyze(self):
        self._slots = {1: (self.parts[0], self.parts[1])}
        
    def abbreviatedDescription(self):
        deg = self.atom(self.morpheme('VxC', self.slots[1][0])).values[0].code
        suf = self.atom(self.morpheme('VxC', self.slots[1][1])).values[0].code
        return '%s_%s' % (suf, deg)
        
    def fullDescription(self):
        deg = self.atom(self.morpheme('VxC', self.slots[1][0])).values[0]
        suf = self.atom(self.morpheme('VxC', self.slots[1][1])).values[0]
        return { 
            'type': 'Affixual adjunct', 
            'categories': ['Type', 'Degree'],
            'Type': { 'code': suf.code, 'name': suf.code },
            'Degree': { 'name': deg.name }
        }