vowels = ['a','â','e','ê','ë','i','î','o','ô','ö','u','û','ü',
		  'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù']

bare_vowels = ['a', 'e', 'i', 'o', 'u']
acute_vowels = ['á', 'é', 'í', 'ó', 'ú']
grave_vowels = ['à', 'è', 'ì', 'ò', 'ù']

consonants_s = ['b', 'c', 'č', 'ç', 'd', 'f', 'g', 'h', 'j', 
				'k', 'l', 'ļ', 'm', 'n', 'ň', 'p', 'q', 
				'r', 'ř', 's', 'š', 't', 'ţ', 'v', 'w', 'x', 'y', 'z', 
				'ż', 'ž']
consonants_d = ['c’', 'cʰ', 'č’', 'čʰ', 'dh', 'k’', 'kʰ', 'p’', 'pʰ', 
				'q’', 'qʰ', 't’', 'tʰ', 'xh']
geminated = ['l', 'm', 'n', 'ň', 'r']
tones = ['\\', '_','/','ˇ','^','¯']
	
def filter_chars(text):
	valid_chars = vowels + consonants_s + tones + ['\'', '’', '-', ' ', 'ʰ']
	return ''.join([x for x in text if x in valid_chars])

def handle_special_chars(s):
	s = s.replace('\'', '’')
	s = s.replace('ch', 'cʰ')
	s = s.replace('kh', 'kʰ')
	s = s.replace('ph', 'pʰ')
	s = s.replace('qh', 'qʰ')
	s = s.replace('th', 'tʰ')
	if s.startswith('-'):
		s = '¯' + s[1:]
	if s.startswith('\\/'):
		s = 'ˇ' + s[2:]
	return s

def remove_accents(s):
	s = s.replace('á', 'a')
	s = s.replace('é', 'e')
	s = s.replace('í', 'i')
	s = s.replace('ó', 'o')
	s = s.replace('ú', 'u')
	s = s.replace('à', 'a')
	s = s.replace('è', 'e')
	s = s.replace('ò', 'o')
	s = s.replace('ì', 'i')
	s = s.replace('ù', 'u')
	return s

def validation(s):
	if s in ('h','w','y','hw','hh','hr','hm','hn','lw','ly','rw','ry','řw','řy'):
		return True
	return False
