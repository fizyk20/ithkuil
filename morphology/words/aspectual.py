from .word import Word
from ..data import ithWordType
from .. import Session  
    
class AspectualAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Aspectual adjunct').first()
    
    def analyze(self):
        self._slots = {1: self.parts[0]}
        
    def abbreviatedDescription(self):
        return 'Aspectual adjunct'
        
    def fullDescription(self):
        return {'type': 'Aspectual adjunct', 'categories': []}
