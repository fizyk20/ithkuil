from .word import Word
from ..data import ithWordType
from .. import Session

class BiasAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Bias adjunct').first()
    
    def analyze(self):
        self._slots = {1: self.parts[0]}
        
    def abbreviatedDescription(self):
        return 'Bias adjunct'
        
    def fullDescription(self):
        return {'type': 'Bias adjunct', 'categories': []}
