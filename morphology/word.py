import abc
from .helpers import *
from .data import *
from morphology import session

def split(s):
	if not s:
		return []
	elif s[0] in tones:
		return [s[0]] + split(s[1:])
	elif s[0] in consonants_s + ['’', 'ʰ', '-']:
		part = ''
		while s and s[0] in consonants_s + ['’', 'ʰ', '-']:
			part += s[0]
			s = s[1:]
		return [part] + split(s)
	elif s[0] in vowels + ['’']:
		part = ''
		while s and s[0] in vowels + ['’']:
			part += s[0]
			s = s[1:]
		return [part] + split(s)
	raise Exception('Something went terribly wrong')

def isVerbalAdjunct(parts):
	if parts[-1][0] in vowels:
		if '-' in parts[-2]:
			return True
	else:
		if '-' in parts[-1]:
			return True
		if len(parts) > 2 and '-' in parts[-3]:
			return True
	return False
	
def isPersonalAdjunct(parts):
	count_consonants = 0
	for p in parts:
		if p[0] not in vowels:
			count_consonants += 1
	if count_consonants == 1 and parts[-1][0] in vowels:
		return True
	if parts[-1][0] in vowels:
		if parts[-2] in ('w','y','h','hw'):
			return True
	else:
		if '’' in parts[-2] and parts[-3] in ('w','y','h','hw'):
			return True
	return False

def isAffixualAdjunct(parts):
	if len(parts) != 2:
		return False
	if parts[0][0] not in vowels or parts[1][0] in vowels:
		return False
	return True

def isAspectualAdjunct(parts):
	if len(parts) != 1:
		return False
	if parts[0][0] not in vowels:
		return False
	return True
	
def isBiasAdjunct(parts):
	if len(parts) != 1:
		return False
	if parts[0][0] in vowels:
		return False
	return True

class Word(metaclass=abc.ABCMeta):
	
	wordType = None
	_slots = None
	
	def __init__(self, word):
		self.word = word
		self.parts = split(word)
		self.type = self.wordType.name
		self.stress = '-2'
		self.tone = '\\'
		
	def __getattr__(self, attr):
		if self._slots and attr in self._slots:
			return self._slots[attr]
		raise AttributeError
	
	@staticmethod
	def fromString(word):
		parts = split(word)
		if isVerbalAdjunct(parts):
			return VerbalAdjunct(word)
		elif isPersonalAdjunct(parts):
			return PersonalAdjunct(word)
		elif isAffixualAdjunct(parts):
			return AffixualAdjunct(word)
		elif isAspectualAdjunct(parts):
			return AspectualAdjunct(word)
		elif isBiasAdjunct(parts):
			return BiasAdjunct(word)
		else:
			return Formative(word)
	
	@abc.abstractmethod
	def describe(self):
		pass
	
	@abc.abstractmethod
	def analyze(self):
		pass
	
	@property
	def slots(self):
		if not self._slots:
			self.analyze()
		return self._slots
	

class Formative(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Formative').first()
	
	def analyzeStress(self):
		parts2 = self.parts[:]
		parts_no_stress = self.parts[:]
		
		for p in self.parts:
			if p[0] not in vowels and '-' not in p:
				parts2.remove(p)
				
		parts3 = []
		for p in parts2:
			parts4 = p.split('’')
			i = self.parts.index(p)
			for p4 in parts4:
				if p4: 
					if len(p4) == 2 and p4[0] == p4[1]:
						parts3.append((i, p4))
					elif len(p4) == 2 and remove_accents(p4[1]) not in ('i','u'):
						parts3.append((i, p4[0]))
						parts3.append((i, p4[1]))
					elif len(p4) == 2 and p4[1] in grave_vowels:
						parts3.append((i, p4[0]))
						parts3.append((i, remove_accents(p4[1])))
					elif len(p4) == 2 and p4[1] in acute_vowels:
						parts3.append((i, p4[0]))
						parts3.append((i, p4[1]))
					else:
						parts3.append((i, p4[0]))
		
		for i in range(len(parts3)-1, -1, -1):
			p = parts3[i][1]
			if len(p)>1 and p[0] == p[1]:
				parts_no_stress[parts3[i][0]] = p[0]
				return str(i-len(parts3)), parts_no_stress
			
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
			
		for i in range(len(parts3)-1, -1, -1):
			p = parts3[i][1]
			if p[0] in grave_vowels:
				parts_no_stress[parts3[i][0]] = remove_accents(parts_no_stress[parts3[i][0]])
				if i == len(parts3)-1:
					try:
						if parts3[-3][1] not in bare_vowels:
							return '-3', parts_no_stress
						elif parts3[-4][1] not in bare_vowels:
							return '-4', parts_no_stress
					except:
						return 'wtf', []
					return 'wtf', []
				elif i == len(parts3)-2:
					try:
						if parts3[-1][1] not in bare_vowels:
							return '-1', parts_no_stress
						elif parts3[-3][1] not in bare_vowels:
							return '-3', parts_no_stress
						elif parts3[-4][1] not in bare_vowels:
							return '-4', parts_no_stress 
					except:
						return 'wtf', []
					return 'wtf', []
				elif i == len(parts3)-3:
					try:
						if parts3[-1][1] not in bare_vowels and parts3[-2][1] not in bare_vowels:
							return '-1', parts_no_stress
						else:
							return '-4', parts_no_stress
					except:
						return 'wtf', []
					return 'wtf', []
			
		return '-2', parts_no_stress
	
	def __init__(self, word):
		super().__init__(word)
		self.stress, self.parts = self.analyzeStress()
		
	def analyze(self, force_cx=False):
		parts = self.parts[:]
		self._slots = {}
		
		# tone
		if parts[0] in tones:
			self.tone = parts[0]
			parts = parts[1:]
		
		# first, we determine if self._slots I-III are filled
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
		# now self._slots I-IV are determined and parts begin with slot V or VII	 
		
		# are self._slots V and VI filled?
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
	
		# now self._slots V and VI are determined and we are at slot VII	
		self._slots['Cr'] = parts[0]
		self._slots['Vc'] = parts[1]
		parts = parts[2:]
		# now we know self._slots VII and VIII
	
		if '’' in self._slots['Vc'] and self._slots['Vc'][-1] != '’':
			# handle xx'V case
			pts = self._slots['Vc'].split('’')
			if pts[1] != 'a' or 'Vr' not in self._slots:
				self._slots['Vr'] = pts[1]
			elif pts[1] != 'a' and 'Vr' in self._slots:
				raise Exception('Stem and Pattern defined twice: in Vr and Vc')
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
			raise Exception('Unexpected slot after Ca/VxC!')
		
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
				raise Exception('Format was specified but there is no incorporated root!')
		
		# if self._slots V and VI are present, but they are not the incorporated root		
		if 5 in self._slots and 6 in self._slots:
			if 'Cv' in self._slots:
				raise Exception('Cv defined twice (in slot I and V)!')
			if 'Vl' in self._slots:
				raise Exception('Vl defined twice (in slot II and VI)!')
			self._slots['Cv'] = self._slots[5]
			self._slots['Vl'] = self._slots[6]
			del self._slots[5]
			del self._slots[6]
			
		if 'Vr' not in self._slots:
			self._slots['Vr'] = 'a'
	
	def describe(self):
		return 'Formative'
	
	
class VerbalAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Verbal adjunct').first()
	
	def analyze(self):
		parts = self.parts[:]
		self._slots = {}
	
		if len(parts)>2 and parts[-2][-1] == '’':
			parts[-2] = parts[-2][:-1]
			self._slots['G'] = parts[-1]
			parts = parts[:-1]
		
		if parts[-1][0] in vowels:
			self._slots['F'] = parts[-1]
			parts = parts[:-1]
			
		if parts[0] in tones:
			self._slots['H'] = parts[0]
			parts = parts[1:]
			
		self._slots['E'] = parts[-1]
		if len(parts) > 1:
			self._slots['D'] = parts[-2]
		if len(parts) > 2:
			self._slots['C'] = parts[-3]
		if len(parts) > 3:
			self._slots['B'] = parts[-4]
		if len(parts) > 4:
			self._slots['A'] = parts[-5]
	
	def describe(self):
		return 'Verbal adjunct'
	

class PersonalAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Personal adjunct').first()
	
	def analyze(self):
		parts = self.parts[:]
		self._slots = {}
	
		if parts[0] in tones:
			self.tone = parts[0]
			parts = parts[1:]
			
		if parts[-1][0] not in vowels:
			self._slots['bias'] = parts[-1]
			parts[-2] = parts[-2][:-1]
			parts = parts[:-1]
			
		if parts[-2] in ('w', 'y', 'h', 'hw'):
			self._slots['Cz'] = parts[-2]
			self._slots['Vz'] = parts[-1]
			if parts[-3][-1] == '’':
				parts[-3] = parts[-3][:-1]
				self._slots['Cz'] = '’' + self._slots['Cz']
			parts = parts[:-2]
			
		self._slots['C1'] = parts[-2]
		self._slots['V1'] = parts[-1]
		parts = parts[:-2]
		
		if (len(self._slots['C1']) == 1 and self._slots['C1'] not in ('g', 'd', 'j', 'ż', 'c', 'b')) or self._slots['C1'] == 'xh':
			#single-referent
			self._slots['CsVs'] = []
			if len(parts) == 1:
				self._slots['V2'] = parts[0]
			else:
				while parts:
					self._slots['CsVs'].append((parts[-1], parts[-2]))
					parts = parts[:-2]
		else:
			#dual-referent
			self._slots['Ck'] = self._slots['C1']
			del self._slots['C1']
			
			self._slots['V2'] = parts[-1]
			parts = parts[:-1]
			if parts:
				self._slots['C2'] = parts[-1]
				parts = parts[:-1]
			if parts:
				self._slots['Vw'] = parts[-1]
		
	def describe(self):
		return 'Personal adjunct'
	

class AffixualAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Affixual adjunct').first()
	
	def analyze(self):
		self._slots = {1: (self.parts[0], self.parts[1])}
		
	def describe(self):
		return 'Affixual adjunct'
	

class AspectualAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Aspectual adjunct').first()
	
	def analyze(self):
		self._slots = {1: self.parts[0]}
		
	def describe(self):
		return 'Aspectual adjunct'
	

class BiasAdjunct(Word):
	
	wordType = session.query(ithWordType).filter(ithWordType.name == 'Bias adjunct').first()
	
	def analyze(self):
		self._slots = {1: self.parts[0]}
		
	def describe(self):
		return 'Bias adjunct'
	