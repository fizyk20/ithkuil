from .word import Word
from ..data import ithWordType
from ..helpers import vowels, tones
from .. import Session

class VerbalAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Verbal adjunct').first()
    
    def analyze(self):
        parts = self.parts[:]
        self._slots = {}
    
        if len(parts)>2 and parts[-2][-1] == '’':
            parts[-2] = parts[-2][:-1]
            self._slots['G'] = parts[-1]
            parts = parts[:-1]
        
        if parts[-1][0] in vowels:
            self._slots['F'] = parts[-1]
            parts = parts[:-1]
            
        if parts[0] in tones:
            self._slots['H'] = parts[0]
            parts = parts[1:]
            
        self._slots['E'] = parts[-1]
        if len(parts) > 1:
            self._slots['D'] = parts[-2]
        if len(parts) > 2:
            self._slots['C'] = parts[-3]
        if len(parts) > 3:
            self._slots['B'] = parts[-4]
        if len(parts) > 4:
            self._slots['A'] = parts[-5]
    
    def abbreviatedDescription(self):
        return 'Verbal adjunct'
    
    def fullDescription(self):
        return {'type': 'Verbal adjunct', 'categories': []}