from .word import Word
from ithkuil.morphology.database import ithWordType, Session
from ..helpers import vowels, tones

class PersonalAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
    
    def analyze(self):
        parts = self.parts[:]
        self._slots = {}
    
        if parts[0] in tones:
            self._slots['[tone]'] = parts[0]
            parts = parts[1:]
            
        if parts[-1][0] not in vowels:
            self._slots['bias'] = parts[-1]
            parts[-2] = parts[-2][:-1]
            parts = parts[:-1]
            
        if parts[-2] in ('w', 'y', 'h', 'hw'):
            self._slots['Cz'] = parts[-2]
            self._slots['Vz'] = parts[-1]
            if parts[-3][-1] == '’':
                parts[-3] = parts[-3][:-1]
                self._slots['Cz'] = '’' + self._slots['Cz']
            parts = parts[:-2]
            
        self._slots['C1'] = parts[-2]
        self._slots['V1'] = parts[-1]
        parts = parts[:-2]
        
        if (len(self._slots['C1']) == 1 and self._slots['C1'] not in ('g', 'd', 'j', 'ż', 'c', 'b')) or self._slots['C1'] == 'xh':
            #single-referent
            self._slots['CsVs'] = []
            if len(parts) == 1:
                self._slots['V2'] = parts[0]
            else:
                while parts:
                    self._slots['CsVs'].append((parts[-1], parts[-2]))
                    parts = parts[:-2]
        else:
            #dual-referent
            self._slots['Ck'] = self._slots['C1']
            del self._slots['C1']
            
            self._slots['V2'] = parts[-1]
            parts = parts[:-1]
            if parts:
                self._slots['C2'] = parts[-1]
                parts = parts[:-1]
            if parts:
                self._slots['Vw'] = parts[-1]
        
    def abbreviatedDescription(self):
        return 'Personal adjunct'
        
    def fullDescription(self):
        return {'type': 'Personal adjunct', 'categories': []}
