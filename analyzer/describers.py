from morphology.models import *
import re

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

def morpheme(word_type, slot, content):
	morphemes = Morpheme.objects.filter(slot__word_type__name=word_type).filter(slot__name=slot).filter(content=content).all()
	if len(morphemes) > 1:
		raise Exception('Too many morphemes')
	elif len(morphemes) == 0:
		return None
	else:
		return morphemes[0]

def describe_formative(slots):
	desc = {'type': 'Formative', 'categories': {}}
	del slots['type']
	# describe each category
	desc['categories']['Root'] = slots['Cr']
	desc['suffixes'] = []
	del slots['Cr']
	
	if 'Cx' in slots:
		desc['categories']['Incorporated root'] = slots['Cx']
		del slots['Cx']
	
	for k in slots:
		# suffixes
		if k == 'VxC':
			for deg, suf in slots[k]:
				mdeg = morpheme('Formative', 'VxC', deg)
				msuf = morpheme('Formative', 'VxC', suf)
				if not msuf or not mdeg:
					return {'error': 'Invalid suffix or degree: %s%s' % (deg, suf)}
				desc['suffixes'].append({'suffix': msuf.values.all()[0], 'degree': mdeg.values.all()[0]})
			continue
		
		morph = morpheme('Formative', k, slots[k])
		if not morph:
			desc['categories'][k] = slots[k]
			continue
		for val in morph.values.all():
			mod = ''
			if k == 'Vp':
				mod = ' (inc)'
			# Assertive illocution in Cv functions as unmarked
			if k == 'Cv' and val.category.name == 'Illocution' and val.code == 'ASR':
				continue
			desc['categories'][val.category.name + mod] = val
	
	# special suffixes
	special = None
	for suf in desc['suffixes']:
		if re.match('FE\d+', suf['suffix'].code):
			num = int(suf['suffix'].code[2:])
			degs = suf['degree'].code.split('/')
			typ = int(degs[0])
			deg = int(degs[1])
			p = ['M', 'U', 'N', 'A']
			conf = ['UNI', 'DPX', 'DCT', 'AGG', 'SEG', 'CPN', 'COH', 'CST', 'MLT']
			desc['categories']['Perspective (inc)'] = CategValue.objects.get(code=p[(num-1) % 4])
			desc['categories']['Configuration (inc)'] = CategValue.objects.get(code=conf[(num-1) / 4 + (typ-1)])
			cases = CategValue.objects.filter(category__name='Case').order_by('id').all()
			form = desc['categories']['Format'].code if 'Format' in desc['categories'] else ''
			case = formats.index(form)*9 + deg-1
			# BEWARE: database-dependent code
			x = case/12
			y = case%12
			desc['categories']['Case (inc)'] = cases[y*6 + x]
			if 'Format' in desc['categories']: del desc['categories']['Format']
			special = suf
			break
			
	if special: desc['suffixes'].remove(special)
	
	cats = desc['categories'].items()	
	cats.sort(key = lambda x: categories.index(x[0]) if x[0] in categories else 2000)
	desc['categories'] = cats
	return desc
			
def describe_word(slots):
	if slots['type'] == 'Formative':
		return describe_formative(slots)
	else:
		return slots
	
