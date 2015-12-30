from .word import Word
from ..data import ithWordType
from .. import Session  

class AffixualAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Affixual adjunct').first()
    
    def analyze(self):
        self._slots = {1: (self.parts[0], self.parts[1])}
        
    def abbreviatedDescription(self):
        return 'Affixual adjunct'
        
    def fullDescription(self):
        return {'type': 'Affixual adjunct', 'categories': []}