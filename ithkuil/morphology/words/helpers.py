from ..helpers import vowels, consonants_s, tones
from ..exceptions import InvalidCharacter

def split(s):
    if not isinstance(s, str):
        raise TypeError('Word should be a string')
    s = s.lower()
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
    raise InvalidCharacter(s[0])

def isVerbalAdjunct(parts):
    if len(parts) < 2:
        return False
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
    if len(parts) < 2:
        return False
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