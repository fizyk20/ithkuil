from .word import Word
from ithkuil.morphology.database import ithWordType, Session
from ..exceptions import AnalysisException

class Formative(Word):

    wordType = Session().query(ithWordType).filter(ithWordType.name == 'Formative').first()

    def analyze(self):
        vc = self.slots['Vc']
        vcparts = [x for x in vc.split('’') if x]
        if len(vcparts) > 1:
            self.slots['Vc'] = vcparts[0] + '’V'
            vr = vcparts[1]
            if 'Vr' in self.slots and self.slots['Vr'] != 'a' and vr != 'a':
                raise AnalysisException('Duplicate Vr: in slots IV and VII!')
            else:
                self.slots['Vr'] = vr

    def fillResult(self, add, suffix):
        if 'Cx' in self.slots:
            add('Cv')
            add('Vl')
        add('Cg')
        add('Cs')
        add('Vr')
        if 'Cx' in self.slots:
            add('Cx')
            add('Vp')
        else:
            add('Cv')
            add('Vl')
        add('Cr')
        add('Vc')
        add('Ci+Vi')
        add('Ca')
        if 'VxC' in self.slots:
            for suf in self.slots['VxC']:
                suffix(suf)
        add('Vf')
        add('Cb')
        add('[tone]')
        add('[stress]')

    def abbreviatedDescription(self):
        desc = []

        def values(slot):
            if slot == 'Cx' or slot == 'Cr':
                return self.slots[slot]
            vals = self.slots_values(slot)
            codes = map(lambda x: x.code, vals)
            return '/'.join(codes)

        def add(slot):
            if slot not in self.slots:
                return
            vals = values(slot)
            if slot == 'Cb' and 'Cb+' in self.slots:
                vals += '+' if self.slots['Cb+'] else ''
            desc.append(vals) 

        def suffix(suf):
            deg = self.atom(self.morpheme('VxC', suf['degree'])).values[0].code
            suf = self.atom(self.morpheme('VxC', suf['type'])).values[0].code
            desc.append('%s_%s' % (suf, deg))

        self.fillResult(add, suffix)

        return '-'.join(desc)

    def fullDescription(self):
        desc = {'type': 'Formative' }

        def values(slot):
            if slot == 'Cx':
                return { 'Incorporated root': self.slots[slot] }
            elif slot == 'Cr':
                return { 'Root': self.slots[slot] }
            vals = self.slots_values(slot)
            result = { x.category.name: {'code': x.code, 'name': x.name} for x in vals }
            if slot == 'Vp':
                result = { k + ' (inc)': v for k, v in result}
            return result

        def add(slot):   
            if slot not in self.slots:
                return
            vals = values(slot)
            if slot == 'Cb' and 'Cb+' in self.slots:
                vals['Bias'] += '+' if self.slots['Cb+'] else ''
            desc.update(vals) 

        def suffix(suf):
            if 'suffixes' not in desc:
                desc['suffixes'] = []
            deg = self.atom(self.morpheme('VxC', suf['degree'])).values[0].name
            suf = self.atom(self.morpheme('VxC', suf['type'])).values[0]
            desc['suffixes'].append({'code': suf.code, 'name': suf.name, 'degree': deg})

        self.fillResult(add, suffix)

        return desc


