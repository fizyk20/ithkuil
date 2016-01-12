from .word import Word
#from .verbal import VerbalAdjunct
from ithkuil.morphology.database import ithWordType, Session

class AspectualAdjunct(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Aspectual adjunct').first()

    def analyze(self):
        pass

    # TODO when database is complete

    def abbreviatedDescription(self):
        #return self.morpheme('F', self.slots[1], VerbalAdjunct.wordType).values[0].code
        return 'Aspectual adjunct'

    def fullDescription(self):
        #mor = self.morpheme('F', self.slots[1], VerbalAdjunct.wordType).values[0]
        return {
            'type': 'Aspectual adjunct',
        #    'categories': ['Aspect'],
        #    'Aspect': {'code': mor.code, 'name': mor.name }
        }
