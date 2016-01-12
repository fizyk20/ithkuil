from .word import Word
from ithkuil.morphology.database import ithWordType, Session

class VerbalAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Verbal adjunct').first()

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
        desc = {'type': 'Verbal adjunct' }

        def values(slot):
            vals = self.slots_values(slot)
            result = { x.category.name: {'code': x.code, 'name': x.name} for x in vals }
            return result

        def add(slot):   
            if slot not in self.slots:
                return
            vals = values(slot)
            if slot == 'Cb' and 'Cb+' in self.slots:
                vals['Bias'] += '+' if self.slots['Cb+'] else ''
            desc.update(vals)

        self.fillResult(add)
