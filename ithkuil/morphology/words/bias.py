from .word import Word
from ithkuil.morphology.database import ithWordType, Session

class BiasAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Bias adjunct').first()

    def analyze(self):
        pass

    def abbreviatedDescription(self):
        return 'Bias adjunct: %s%s' % (self.slots_values('Cb')[0].code, '+' if self.slots['Cb+'] else '')

    def fullDescription(self):
        mor = self.slots_values('Cb')[0]
        return {
            'type': 'Bias adjunct',
            'Bias': {'code': mor.code + '+' if self.slots['Cb+'] else '', 'name': mor.name}
        }
