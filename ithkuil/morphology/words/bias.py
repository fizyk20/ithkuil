from .word import Word
from .formative import Formative
from ithkuil.morphology.database import ithWordType, Session

class BiasAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Bias adjunct').first()

    def analyze(self):
        pass

    def abbreviatedDescription(self):
        return 'Bias adjunct: %s%s' % (self.morpheme('Cb', self.slots[1], Formative.wordType).values[0].code, '+' if self.slots['Cb+'] else '')

    def fullDescription(self):
        mor = self.morpheme('Cb', self.slots[1], Formative.wordType).values[0]
        return {
            'type': 'Bias adjunct',
            'categories': ['Bias'],
            'Bias': {'code': mor.code, 'name': mor.name}
        }
