from .word import Word
#from .verbal import VerbalAdjunct
from ..data import ithWordType
from .. import Session  
    
class AspectualAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Aspectual adjunct').first()
    
    def analyze(self):
        self._slots = {1: self.parts[0]}
    
    # TODO when database is complete
    
    def abbreviatedDescription(self):
        #return self.morpheme('F', self.slots[1], VerbalAdjunct.wordType).values[0].code
        return 'Aspectual adjunct'
        
    def fullDescription(self):
        #mor = self.morpheme('F', self.slots[1], VerbalAdjunct.wordType).values[0]
        return {
            'type': 'Aspectual adjunct',
        #    'categories': ['Aspect'],
        #    'Aspect': {'code': mor.code, 'name': mor.name }
        }
