from .word import Word
from ithkuil.morphology.database import ithWordType, Session

class Formative(Word):
	
	wordType = Session().query(ithWordType).filter(ithWordType.name == 'Formative').first()
	
	categories = [
		'Root',
		'Stem and Pattern',
		'Designation',
		'Incorporated root',
		'Stem and Pattern (inc)',
		'Designation (inc)',
		'Perspective (inc)',
		'Configuration (inc)',
		'Case (inc)',
		'Format',
		'Relation',
		'Function',
		'Case',
		'Essence',
		'Extension',
		'Perspective',
		'Affiliation',
		'Configuration',
		'Context',
		'Aspect',
		'Mood',
		'Phase',
		'Sanction',
		'Illocution',
		'Version',
		'Valence',
		'Bias'
	]
	
	formats = [
		'',
		'SCH',
		'ISR',
		'ATH',
		'RSL',
		'SBQ',
		'CCM',
		'OBJ'
	]
	
	def analyze(self):
		pass
			
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
				
		def suffix(suf):
			deg = self.atom(self.morpheme('VxC', suf[0])).values[0].code
			suf = self.atom(self.morpheme('VxC', suf[1])).values[0].code
			desc.append('%s_%s' % (suf, deg))
			
		self.fillResult(add, suffix)
		
		return '-'.join(desc)
	
	def fullDescription(self):
		desc = {'type': 'Formative', 'categories': self.categories }
		
		def values(atom):
			if isinstance(atom, str):
				return { 'other': atom }
			vals = { x.category.name: {'code': x.code, 'name': x.name} for x in atom.values }
			return vals
		
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
				mor = self.morpheme(slot, val[0])
				val = self.atom(mor).values[0]
				desc['Bias'] = { 'code': mor.code, 'name': '%s%s' % (mor.name, '+' if val[1] else '')}
				return
			
			if slot in self.slots:
				vals = values(self.atom(self.morpheme(slot, self.slots[slot])))
				# handle roots (primary and incorporated)
				if 'other' in vals:
					if slot == 'Cr':
						desc['Root'] = {'name': vals['other']}
						del vals['other']
					elif slot == 'Cx':
						desc['Incorporated root'] = {'name': vals['other']}
						del vals['other']
					elif 'other' in desc:
						desc['other'] = {'name': '%s, %s' % (desc['other'], vals['other'])}
						del vals['other']
				# handle categories for the incorporated root
				if slot == 'Cx' or slot == 'Vp':
					keys = list(vals.keys())
					for k in keys:
						vals[k + ' (inc)'] = vals[k]
						del vals[k]
				desc.update(vals)
				
		def suffix(suf):
			if 'suffixes' not in desc:
				desc['suffixes'] = []
			deg = self.atom(self.morpheme('VxC', suf[0])).values[0].name
			suf = self.atom(self.morpheme('VxC', suf[1])).values[0]
			desc['suffixes'].append({'code': suf.code, 'name': suf.name, 'degree': deg})
			
		self.fillResult(add, suffix)
		
		return desc
	
	
