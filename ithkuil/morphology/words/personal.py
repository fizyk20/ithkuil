from .word import Word
from ithkuil.morphology.database import ithWordType, Session
from ithkuil.morphology.exceptions import AnalysisException

class PersonalAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
    
    defaults = {
        '[tone]': '\\',
        'Cz': 'w',
        'Vz': 'a'
    }
    
    def __init__(self, *args):
        self.spoof_defaults = False
        super().__init__(*args)
        
    def slot_map(self, slot):
        if slot == 'Vc2':
            return 'Vc'
        else:
            return slot

    def analyze(self):
        if 'Vc' in self.slots and 'Cz' in self.slots:
            pass

    def fillResult(self, add, suffix):
        if 'C1' in self.slots:
            if 'VxC' in self.slots:
                for suf in self.slots['VxC']:
                    suffix(suf)
            if 'Vc2' in self.slots:
                add('Vc2', '[tone]')
            add('C1', '[tone]')
            add('Vc', 'Cz')
            add('Cz')
            add('Vz', '[tone]')
            add('Cb')
        else:
            add('Ck', '[tone]')
            
    @property
    def slots(self):
        if self.spoof_defaults:
            copy = { k:v for k,v in self._slots.items() }
            copy.update(self.defaults)
            return copy
        return self._slots

    def abbreviatedDescription(self):
        desc = []

        def values(*slots):
            vals = self.slots_values(*slots)
            codes = map(lambda x: x.code, vals)
            return '/'.join(codes)

        def add(*slots):
            filtered_slots = [slot for slot in slots if slot in self.slots]
            if not filtered_slots:
                return
            vals = None
            try:
                vals = values(*filtered_slots)
            except AnalysisException:
                self.spoof_defaults = True
                vals = values(*slots)
                self.spoof_defaults = False
            if slots == ['Cb'] and 'Cb+' in self.slots:
                vals += '+' if self.slots['Cb+'] else ''
            desc.append(vals) 

        def suffix(suf):
            deg = self.atom(self.morpheme('VxC', suf['degree'])).values[0].code
            suf = self.atom(self.morpheme('VxC', suf['type'])).values[0].code
            desc.append('%s_%s' % (suf, deg))

        self.fillResult(add, suffix)

        return '-'.join(desc)

    def fullDescription(self):
        return {'type': 'Personal adjunct', 'categories': []}
