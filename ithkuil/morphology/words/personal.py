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
    
    categories = [
        'Configuration 2',
        'Affiliation 2',
        'Case 2',
        'Personal referent',
        'Personal referent 2',
        'Case',
        'Affiliation',
        'Configuration',
        'Essence',
        'Bias'
    ]
    
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

    def fillResult(self, add, add_dict, suffix):
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
            add('Vw')
            add('C2')
            if 'Vc2' in self.slots:
                add_dict({'Vc2': self.slots['Vc2'], '[tone]': '\\'})
            add('Ck', '[tone]')
            if 'Vc' in self.slots:
                add_dict({'Vc': self.slots['Vc'], '[tone]': '\\'})
            add('Cz')
            if 'Vz' in self.slots:
                add_dict({'Vz': self.slots['Vz'], '[tone]': '\\'})
            add('Cb')
            
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
            
        def add_dict(slots):
            vals = self.slots_values_dict(slots)
            codes = map(lambda x: x.code, vals)
            vals = '/'.join(codes)
            desc.append(vals)

        def suffix(suf):
            deg = self.atom(self.morpheme('VxC', suf['degree'])).values[0].code
            suf = self.atom(self.morpheme('VxC', suf['type'])).values[0].code
            desc.append('%s_%s' % (suf, deg))

        self.fillResult(add, add_dict, suffix)

        return '-'.join(desc)

    def fullDescription(self):
        desc = { 'type': 'Personal adjunct', 'categories': self.categories }
        
        def category_name(name, slots):
            if name == 'Case' and 'Vc2' in slots:
                return 'Case 2'
            elif name == 'Configuration' and 'Vw' in slots:
                return 'Configuration 2'
            elif name == 'Affiliation' and 'C2' in slots:
                return 'Affiliation 2'
            else:
                return name

        def values(*slots):
            vals = self.slots_values(*slots)
            result = { category_name(x.category.name, slots): {'code': x.code, 'name': x.name} for x in vals }
            if 'Ck' in slots:
                for v in vals:
                    if v.category.name == 'Personal referent' and result['Personal referent']['code'] != v.code:
                        result['Personal referent 2'] = { 'code': v.code, 'name': v.name }
            return result

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
            if 'Bias' in vals and 'Cb+' in self.slots:
                vals['Bias'] += '+' if self.slots['Cb+'] else ''
            desc.update(vals)
            
        def add_dict(slots):
            vals = self.slots_values_dict(slots)
            desc.update({ category_name(x.category.name, slots): {'code': x.code, 'name': x.name} for x in vals })

        def suffix(suf):
            if 'suffixes' not in desc:
                desc['suffixes'] = []
            deg = self.atom(self.morpheme('VxC', suf['degree'])).values[0].code
            suf = self.atom(self.morpheme('VxC', suf['type'])).values[0].code
            desc['suffixes'].append({'code': suf.code, 'name': suf.name, 'degree': deg})

        self.fillResult(add, add_dict, suffix)
        
        return desc

