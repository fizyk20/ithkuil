from .word import Word
from ..data import ithWordType, Session
from ..helpers import vowels, tones

class VerbalAdjunct(Word):
    
    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Verbal adjunct').first()
    
    def analyze(self):
        parts = self.parts[:]
        self._slots = {}
    
        if len(parts)>2 and parts[-2][-1] == '’':
            parts[-2] = parts[-2][:-1]
            self._slots['Cb'] = parts[-1]
            parts = parts[:-1]
        
        if parts[-1][0] in vowels:
            self._slots['Vs'] = parts[-1]
            parts = parts[:-1]
            
        if parts[0] in tones:
            self._slots['[tone]'] = parts[0]
            parts = parts[1:]
            
        self._slots['Cs'] = parts[-1]
        if len(parts) > 1:
            self._slots['Vm'] = parts[-2]
        if len(parts) > 2:
            self._slots['Cv'] = parts[-3]
        if len(parts) > 3:
            self._slots['Ve'] = parts[-4]
        if len(parts) > 4:
            self._slots['Cl'] = parts[-5]
            
    def fillResult(self, add):
        add('Cl')
        add('Ve')
        add('Cv')
        add('Vm')
        add('Cs')
        add('Vs')
        add('Cb')
        add('[tone]')
    
    def abbreviatedDescription(self):
        desc = []
        
        def values(morph):
            if isinstance(morph, str):
                return morph
            vals = [x.code for x in morph.values]
            return '/'.join(vals)
        
        def add(slot):
            # handle biases
            if slot == 'Cb' and slot in self.slots:
                val = self.slots[slot]
                if len(val) > 1 and val[-1] == val[-2]:
                    val = (val[:-1], True)
                elif val == 'xxh':
                    val = ('xh', True)
                else:
                    val = (val, False)
                desc.append('%s%s' % (self.morpheme(slot, val[0]).values[0].code, '+' if val[1] else ''))
                return
            
            if slot in self.slots:
                desc.append(values(self.morpheme(slot, self.slots[slot])))
            
        self.fillResult(add)
        
        return '-'.join(desc)
    
    def fullDescription(self):
        return {'type': 'Verbal adjunct', 'categories': []}