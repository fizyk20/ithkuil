from .word import Word
from ithkuil.morphology.database import ithWordType, Session

class VerbalAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Verbal adjunct').first()
    
    categories = [
        'Valence',
        'Level',
        'Phase',
        'Sanction',
        'Illocution',
        'Modality',
        'Aspect',
        'Aspect 2',
        'Bias',
        'Extension'
    ]

    def analyze(self):
        pass

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

        def values(slot):
            vals = self.slots_values(slot)
            codes = map(lambda x: x.code, vals)
            return '/'.join(codes)

        def add(slot):
            if slot not in self.slots:
                return
            vals = values(slot)
            if slot == 'Cb' and 'Cb+' in self.slots:
                vals += '+' if self.slots['Cb+'] else ''
            if vals != '(NO-MOD)':
                desc.append(vals)

        self.fillResult(add)

        return '-'.join(desc)

    def fullDescription(self):
        desc = { 'type': 'Verbal adjunct', 'categories': self.categories }

        def values(slot):
            vals = self.slots_values(slot)
            result = { x.category.name: {'code': x.code, 'name': x.name} for x in vals }
            return result

        def add(slot):   
            if slot not in self.slots:
                return
            vals = values(slot)
            if 'Modality' in vals and vals['Modality']['code'] == '(NO-MOD)':
                del vals['Modality']
            if slot == 'Cb' and self.slots.get('Cb+'):
                vals['Bias']['code'] += '+'
                vals['Bias']['name'] += '+'
            if 'Aspect' in vals and 'Aspect' in desc:
                vals['Aspect 2'] = vals['Aspect']
                del vals['Aspect']
            desc.update(vals)

        self.fillResult(add)
        
        return desc

