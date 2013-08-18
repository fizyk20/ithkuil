from morphology.models import *
import re

def morpheme(word_type, slot, content):
	morphemes = Morpheme.objects.filter(slot__word_type__name=word_type).filter(slot__name=slot).filter(content=content).all()
	if len(morphemes) > 1:
		raise Exception('Too many morphemes')
	elif len(morphemes) == 0:
		return None
	else:
		return morphemes[0]
	
##########################################################
#
# Formatives
#
##########################################################

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

def morph_abbrevs_formative(abbrev):
	result = ''
	
	if 'Cv' in abbrev and 'Cx' in abbrev:
		result = '%s/%s' % (abbrev['Cv']['Phase'].code, abbrev['Cv']['Sanction'].code)
		if 'Illocution' in abbrev['Cv']:
			result += '/' + abbrev['Cv']['Illocution'].code
			
	if 'Vl' in abbrev and 'Cx' in abbrev:
		if result: result += '-'		
		result += abbrev['Vl']['Valence'].code
			
	if 'Cg' in abbrev:
		if result: result += '-'
		result += abbrev['Cg']['Validation'].code
		
	if 'Cs' in abbrev:
		if result: result += '-'
		result += abbrev['Cs']['Aspect'].code
		if 'Mood' in abbrev['Cs']:
			result += '/' + abbrev['Cs']['Mood'].code
		
	if result: result += '-'	
	result += '%s/%s' % (abbrev['Vr']['Function'].code, abbrev['Vr']['Stem and Pattern'].code)
	
	if 'Cv' in abbrev and 'Cx' not in abbrev:
		result += '-%s/%s' % (abbrev['Cv']['Phase'].code, abbrev['Cv']['Sanction'].code)
		if 'Illocution' in abbrev['Cv']:
			result += '/' + abbrev['Cv']['Illocution'].code
		result += '-%s' % abbrev['Vl']['Valence'].code
		
	if 'Cx' in abbrev:	
		result += '-%s-%s/%s' % (abbrev['Cx']['root'], abbrev['Vp']['Stem and Pattern'].code, abbrev['Vp']['Designation'].code)
		
	result += '-%s-%s' % (abbrev['Cr']['root'], abbrev['Vc']['Case'].code)
	
	if 'Ci+Vi' in abbrev:
		result += '-%s/%s' % (abbrev['Ci+Vi']['Illocution'].code, abbrev['Ci+Vi']['Mood'].code)
		
	result += '-%s/%s/%s/%s/%s' % (abbrev['Ca']['Essence'].code, abbrev['Ca']['Extension'].code,
				abbrev['Ca']['Perspective'].code, abbrev['Ca']['Affiliation'].code,
				abbrev['Ca']['Configuration'].code)
				
	if 'VxC' in abbrev:
		for suf, deg in abbrev['VxC']['list']:
			result += '-%s_%s' % (suf.code, deg.code)
			
	if 'Vf' in abbrev:
		if abbrev['Vf']['Context'].code != 'EXS' or 'Format' in abbrev['Vf']:
			result += '-' + abbrev['Vf']['Context'].code
		if 'Format' in abbrev['Vf']:
			result += '/' + abbrev['Vf']['Format'].code
			
	if 'Cb' in abbrev:
		result += '-' + abbrev['Cb']['Bias'].code
		
	if '[tone]' in abbrev:
		result += '-' + abbrev['[tone]']['Version'].code
		
	result += '-%s/%s' % (abbrev['[stress]']['Designation'].code, abbrev['[stress]']['Relation'].code)
	
	return result

def describe_formative(slots):
	desc = {'type': 'Formative', 'categories': {}}
	del slots['type']
	abbrev = {}	# for abbreviations
	
	for k in slots:
		# root
		abbrev[k] = {}
		if k == 'Cr':
			desc['categories']['Root'] = slots['Cr']
			desc['suffixes'] = []
			abbrev['Cr']['root'] = slots['Cr']
			continue
			
		# incorporated root
		if k == 'Cx':
			desc['categories']['Incorporated root'] = slots['Cx']
			abbrev['Cx']['root'] = slots['Cx']
			continue
			
		# suffixes
		if k == 'VxC':
			abbrev['VxC']['list'] = []
			desc['suffixes'] = []
			for deg, suf in slots[k]:
				mdeg = morpheme('Formative', 'VxC', deg).values.all()[0]
				msuf = morpheme('Formative', 'VxC', suf).values.all()[0]
				if not msuf or not mdeg:
					return {'error': 'Invalid suffix or degree: %s%s' % (deg, suf)}
				desc['suffixes'].append({'suffix': msuf, 'degree': mdeg})
				abbrev['VxC']['list'].append((msuf, mdeg))
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
			# Factual mood in Cs = unmarked
			if k == 'Cs' and val.category.name == 'Mood' and val.code == 'FAC':
				continue
			desc['categories'][val.category.name + mod] = val
			abbrev[k][val.category.name] = val
	
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
	
	desc['abbrev'] = morph_abbrevs_formative(abbrev)
	
	cats = desc['categories'].items()	
	cats.sort(key = lambda x: categories.index(x[0]) if x[0] in categories else 2000)
	desc['categories'] = cats
	return desc
	
##########################################################
#
# Main function
#
##########################################################
			
def describe_word(slots):
	if slots['type'] == 'Formative':
		return describe_formative(slots)
	else:
		return {'categories': slots.items()}
	
