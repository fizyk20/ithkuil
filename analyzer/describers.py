from morphology.models import *

def morpheme(word_type, slot, content):
	morphemes = Morpheme.objects.filter(slot__word_type__name=word_type).filter(slot__number=slot).filter(content=content).all()
	if len(morphemes) > 1:
		raise Exception('Too many morphemes')
	elif len(morphemes) == 0:
		return None
	else:
		return morphemes[0]

def describe_formative(slots):
	desc = {'type': 'Formative'}
	del slots['type']
	# describe each category
	desc['categories'] = [('Root', slots['VII'])]
	desc['suffixes'] = []
	del slots['VII']
	
	if 'type5' in slots and slots['type5'] == 'Cx':
		desc['categories'].append(('Incorporated root', slots['V']))
		del slots['type5']
		del slots['V']
	
	for k in slots:
		# suffixes
		if k == 'XI':
			for deg, suf in slots[k]:
				mdeg = morpheme('Formative', 'XI', deg)
				msuf = morpheme('Formative', 'XI', suf)
				if not msuf or not mdeg:
					return {'error': 'Invalid suffix or degree: %s%s' % (deg, suf)}
				desc['suffixes'].append({'suffix': msuf, 'degree': mdeg})
			continue
		
		morph = morpheme('Formative', k, slots[k])
		if not morph:
			desc['categories'].append((k, slots[k]))
			continue
		for val in morph.values.all():
			desc['categories'].append((val.category.name, val))
	return desc
			
def describe_word(slots):
	if slots['type'] == 'Formative':
		return describe_formative(slots)
	else:
		return slots
	
