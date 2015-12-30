from .word import Word
from ..data import ithWordType
from ..helpers import vowels, grave_vowels, acute_vowels, bare_vowels, remove_accents, tones, validation
from ..exceptions import AnalysisException, InvalidStress
from .. import Session

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
	
	def analyzeStress(self):
		parts2 = self.parts[:]
		parts_no_stress = self.parts[:]
		
		# drop non-syllabic parts
		for p in self.parts:
			if p[0] not in vowels and '-' not in p:
				parts2.remove(p)
		
		# split into syllables	
		parts3 = []
		for p in parts2:
			parts4 = p.split('’')	# sometimes a part may consist of more than one syllable
			i = self.parts.index(p)
			for p4 in parts4:
				if p4: 
					# case: doubled vowel
					if len(p4) == 2 and p4[0] == p4[1]:
						parts3.append((i, p4))
					# case: two vowels, not a diphthong
					elif len(p4) == 2 and remove_accents(p4[1]) not in ('i','u'):
						parts3.append((i, p4[0]))
						parts3.append((i, p4[1]))
					# case: grave accent on second vowel (marking not a diphthong)
					elif len(p4) == 2 and p4[1] in grave_vowels:
						parts3.append((i, p4[0]))
						parts3.append((i, remove_accents(p4[1])))
					# case: acute accent on second vowel
					elif len(p4) == 2 and p4[1] in acute_vowels:
						parts3.append((i, p4[0]))
						parts3.append((i, p4[1]))
					# any other case
					else:
						parts3.append((i, p4[0]))
		
		# check for the easiest case of doubled vowel
		for i in range(len(parts3)-1, -1, -1):
			p = parts3[i][1]
			if len(p)>1 and p[0] == p[1]:
				parts_no_stress[parts3[i][0]] = p[0]
				return str(i-len(parts3)), parts_no_stress
		
		# if there is an acute accent somewhere, this is the stressed syllable	
		for i in range(len(parts3)-1, -1, -1):
			p = parts3[i][1]
			if p[0] in acute_vowels:
				part = parts_no_stress[parts3[i][0]]
				if p[0] in ('í', 'ú') and part.index(p[0]) > 0 and part[part.index(p[0])-1] in ('a','e','i','o','u','ö','ë'):
					part = part.replace(p[0], grave_vowels[acute_vowels.index(p[0])])
					parts_no_stress[parts3[i][0]] = part
				else:
					parts_no_stress[parts3[i][0]] = remove_accents(parts_no_stress[parts3[i][0]])
				return str(i-len(parts3)), parts_no_stress
		
		# the hardest case - grave accent	
		for i in range(len(parts3)-1, -1, -1):
			p = parts3[i][1]
			if p[0] in grave_vowels:
				parts_no_stress[parts3[i][0]] = remove_accents(parts_no_stress[parts3[i][0]])
				# grave accent on the ultimate syllable
				if i == len(parts3)-1:
					try:
						if parts3[-3][1] not in bare_vowels:
							return '-3', parts_no_stress
						elif parts3[-4][1] not in bare_vowels:
							return '-4', parts_no_stress
					except:
						pass
					raise InvalidStress(p)
				# grave accent on the penultimate syllable
				elif i == len(parts3)-2:
					try:
						if parts3[-1][1] not in bare_vowels:
							return '-1', parts_no_stress
						elif parts3[-3][1] not in bare_vowels:
							return '-3', parts_no_stress
						elif parts3[-4][1] not in bare_vowels:
							return '-4', parts_no_stress 
					except:
						pass
					raise InvalidStress(p)
				# grave accent on the antepenultimate syllable
				elif i == len(parts3)-3:
					try:
						if parts3[-1][1] not in bare_vowels and parts3[-2][1] not in bare_vowels:
							return '-1', parts_no_stress
						else:
							return '-4', parts_no_stress
					except:
						pass
					raise InvalidStress(p)
		
		# by default, return penultimate stress
		return '-2', parts_no_stress
	
	def __init__(self, word):
		super().__init__(word)
		self.stress, self.parts = self.analyzeStress()
		
	def analyze(self, force_cx=False):
		parts = self.parts[:]
		
		self._slots = { '[stress]': self.stress }
		# tone
		if parts[0] in tones:
			self._slots['[tone]'] = parts[0]
			parts = parts[1:]
		
		# first, we determine if slots I-III are filled
		if parts[0][0] in vowels:
			if validation(parts[1]) or '-' in parts[1]:
				self._slots['Vl'] = parts[0]
				if validation(parts[1]):
					self._slots['Cg'] = parts[1]
				else:
					self._slots['Cs'] = parts[1]
				self._slots['Vr'] = parts[2]
				parts = parts[3:]
			else:
				self._slots['Vr'] = parts[0]
				parts = parts[1:]
		else:
			# is slot I filled?
			if '-' in parts[2]:
				self._slots['Cv'] = parts[0]
				self._slots['Vl'] = parts[1]
				self._slots['Cs'] = parts[2]
				self._slots['Vr'] = parts[3]
				parts = parts[4:]
			# if not, do we begin with slot III?
			elif validation(parts[0]) or '-' in parts[0]:
				if validation(parts[0]):
					self._slots['Cg'] = parts[0]
				else:
					self._slots['Cs'] = parts[0]
				self._slots['Vr'] = parts[1]
				parts = parts[2:]
		# now slots I-IV are determined and parts begin with slot V or VII	 
		
		# are slots V and VI filled?
		# check for glottal stop:
		if 'Vr' in self._slots and self._slots['Vr'][-1] == '’':
			self._slots[5] = parts[0]
			self._slots[6] = parts[1]
			parts = parts[2:]
			self._slots['Vr'] = self._slots['Vr'][:-1]
	
		# if there was no glottal stop, check -wë-
		try:
			if 5 not in self._slots:
				for i in range(len(parts)):
					if parts[i] in ('w', 'y', 'h', 'hw') and i != 2:
						self._slots[5] = parts[0]
						self._slots[6] = parts[1]
						parts = parts[2:]
						break
		except:
			pass
			
		# last - check format
		if parts[-1][0] in vowels:
			self._slots['Vf'] = parts[-1]
			parts = parts[:-1]
		elif parts[-2][-1] == '’' and len(parts)-2 > 1:
			self._slots['Vf'] = parts[-2][:-1]
			self._slots['Cb'] = parts[-1]
			parts = parts[:-2]
		else:
			self._slots['Vf'] = 'a'
			
		if 5 not in self._slots and (self._slots['Vf'] not in ('a', 'i', 'e', 'u') or force_cx):
			self._slots[5] = parts[0]
			self._slots[6] = parts[1]
			parts = parts[2:]
	
		# now slots V and VI are determined and we are at slot VII	
		self._slots['Cr'] = parts[0]
		self._slots['Vc'] = parts[1]
		parts = parts[2:]
		# now we know slots VII and VIII
	
		if '’' in self._slots['Vc'] and self._slots['Vc'][-1] != '’':
			# handle xx'V case
			pts = self._slots['Vc'].split('’')
			if pts[1] != 'a' or 'Vr' not in self._slots:
				self._slots['Vr'] = pts[1]
			elif pts[1] != 'a' and 'Vr' in self._slots:
				raise AnalysisException('Stem and Pattern defined twice: in Vr and Vc')
			self._slots['Vc'] = pts[0] + '’V'
	
		# check for slot IX
		if parts[0] in ('w', 'y', 'h', 'hw'):
			if parts[0] == 'hw' and len(self._slots['Vc']) > 1 and self._slots['Vc'][-1] == 'i' and self._slots['Vc'][-2] != '’':
				self._slots['Ci+Vi'] = 'y' + parts[1]
			elif parts[0] == 'hw' and self._slots['Vc'] in ('a','e','i','o','ö','ë'):
				self._slots['Ci+Vi'] = 'w' + parts[1]
				self._slots['Vc'] = self._slots['Vc'] + 'u'
			else:
				self._slots['Ci+Vi'] = parts[0] + parts[1]
			parts = parts[2:]
		
		# slot X	
		self._slots['Ca'] = parts[0]
		parts = parts[1:]
	
		# suffixes
		self._slots['VxC'] = []
		while len(parts) > 1:
			self._slots['VxC'].append((parts[0], parts[1]))
			parts = parts[2:]
		
		if parts:
			raise AnalysisException('Unexpected slot after Ca/VxC!')
		
		fe_suffix = False
		for _, typ in self._slots['VxC']:
			if typ in ['tt', 'pk', 'qq', 'tk',
						'st’', 'sp’', 'sq’', 'sk’',
						'št’', 'šp’', 'šq’', 'šk’']:
				fe_suffix = True
				break
				
		if fe_suffix and 5 not in self._slots:
			return self.analyze(True)
		
		# if there is format or format expansion suffix		
		if fe_suffix or self._slots['Vf'] not in ('a', 'i', 'e', 'u'):
			if 5 in self._slots and 6 in self._slots:
				self._slots['Cx'] = self._slots[5]
				self._slots['Vp'] = self._slots[6]
				del self._slots[6]
				del self._slots[5]
			else:
				raise AnalysisException('Format was specified but there is no incorporated root!')
		
		# if slots V and VI are present, but they are not the incorporated root		
		if 5 in self._slots and 6 in self._slots:
			if 'Cv' in self._slots:
				raise AnalysisException('Cv defined twice (in slot I and V)!')
			if 'Vl' in self._slots:
				raise AnalysisException('Vl defined twice (in slot II and VI)!')
			self._slots['Cv'] = self._slots[5]
			self._slots['Vl'] = self._slots[6]
			del self._slots[5]
			del self._slots[6]
			
		if 'Vr' not in self._slots:
			self._slots['Vr'] = 'a'
			
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
		
		def values(morph):
			if isinstance(morph, str):
				return morph
			vals = [x.code for x in morph.values]
			return '/'.join(vals)
		
		def add(slot):
			# handle biases
			if slot == 'Cb':
				val = self.slots[slot]
				if len(val) > 1 and val[-1] == val[-2]:
					val = (val[:-1], True)
				elif val == 'xxh':
					val = ('xh', True)
				else:
					val = (val, False)
				desc.append('%s%s' % (self.morpheme(slot, val[0]).values[0].code, '+' if val[1] else ''))
				return
			
			if slot in self.slots:
				desc.append(values(self.morpheme(slot, self.slots[slot])))
				
		def suffix(suf):
			deg = self.morpheme('VxC', suf[0]).values[0].code
			suf = self.morpheme('VxC', suf[1]).values[0].code
			desc.append('%s_%s' % (suf, deg))
			
		self.fillResult(add, suffix)
		
		return '-'.join(desc)
	
	def fullDescription(self):
		desc = {'type': 'Formative', 'categories': self.categories }
		
		def values(morph):
			if isinstance(morph, str):
				return { 'other': morph }
			vals = { x.category.name: {'code': x.code, 'name': x.name} for x in morph.values }
			return vals
		
		def add(slot):
			# handle biases
			if slot == 'Cb':
				val = self.slots[slot]
				if len(val) > 1 and val[-1] == val[-2]:
					val = (val[:-1], True)
				elif val == 'xxh':
					val = ('xh', True)
				else:
					val = (val, False)
				mor = self.morpheme(slot, val[0]).values[0]
				desc['Bias'] = { 'code': mor.code, 'name': '%s%s' % (mor.name, '+' if val[1] else '')}
				return
			
			if slot in self.slots:
				vals = values(self.morpheme(slot, self.slots[slot]))
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
			deg = self.morpheme('VxC', suf[0]).values[0].name
			suf = self.morpheme('VxC', suf[1]).values[0]
			desc['suffixes'].append({'code': suf.code, 'name': suf.name, 'degree': deg})
			
		self.fillResult(add, suffix)
		
		return desc
	
	
