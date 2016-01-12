from .word import Word
from ithkuil.morphology.database import ithWordType, Session
from ..helpers import vowels, tones

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

        def values(atom):
            if isinstance(atom, str):
                return atom
            vals = [x.code for x in atom.values]
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
                morph = self.morpheme(slot, val[0])
                desc.append('%s%s' % (self.atom(morph).values[0].code, '+' if val[1] else ''))
                return

            if slot in self.slots:
                desc.append(values(self.atom(self.morpheme(slot, self.slots[slot]))))

        self.fillResult(add)

        return '-'.join(desc)

    def fullDescription(self):
        return {'type': 'Verbal adjunct', 'categories': []}