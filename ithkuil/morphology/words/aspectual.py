from .word import Word
from ithkuil.morphology.database import ithWordType, Session

class AspectualAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Aspectual adjunct').first()

    def analyze(self):
        pass

    def abbreviatedDescription(self):
        return self.slots_values('Vs')[0].code

    def fullDescription(self):
        val = self.slots_values('Vs')[0]
        return {
            'type': 'Aspectual adjunct',
            'Aspect': {'code': val.code, 'name': val.name }
        }
