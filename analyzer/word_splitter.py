#-*- coding: utf-8 -*-
vowels = [u'a',u'â',u'e',u'ê',u'ë',u'i',u'î',u'o',u'ô',u'ö',u'u',u'û',u'ü',
          u'á', u'é', u'í', u'ó', u'ú', u'à', u'è', u'ì', u'ò', u'ù']

bare_vowels = [u'a', u'e', u'i', u'o', u'u']
acute_vowels = [u'á', u'é', u'í', u'ó', u'ú']
grave_vowels = [u'à', u'è', u'ì', u'ò', u'ù']

consonants_s = [u'b', u'c', u'č', u'ç', u'd', u'f', u'g', u'h', u'j', 
              u'k', u'l', u'ļ', u'm', u'n', u'ň', u'p', u'q', 
              u'r', u'ř', u's', u'š', u't', u'ţ', u'v', u'w', u'x', u'y', u'z', 
              u'ż', u'ž']
consonants_d = [u'c’', u'cʰ', u'č’', u'čʰ', u'dh', u'k’', u'kʰ', u'p’', u'pʰ', 
                u'q’', u'qʰ', u't’', u'tʰ', u'xh']
geminated = [u'l', u'm', u'n', u'ň', u'r']
tones = [u'_',u'/',u'ˇ',u'^',u'¯']

def remove_accents(s, preserve=False):
    s = s.replace(u'á', u'a')
    s = s.replace(u'é', u'e')
    s = s.replace(u'í', u'i')
    s = s.replace(u'ó', u'o')
    s = s.replace(u'ú', u'u')
    s = s.replace(u'à', u'a')
    s = s.replace(u'è', u'e')
    s = s.replace(u'ò', u'o')
    s = s.replace(u'ì', u'i')
    s = s.replace(u'ù', u'u')
    return s

def validation(s):
    if s in (u'h',u'w',u'y',u'hw',u'hh',u'hr',u'hm',u'hn',u'lw',u'ly',u'rw',u'ry',u'řw',u'řy'):
        return True
    return False

def is_verbal_adjunct(parts):
    if parts[-1][0] in vowels:
        if '-' in parts[-2]:
            return True
    else:
        if '-' in parts[-1]:
            return True
        if len(parts) > 2 and '-' in parts[-3]:
            return True
    return False

def is_personal_adjunct(parts):
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
        if u'’' in parts[-2] and parts[-3] in ('w','y','h','hw'):
            return True
    return False

def is_affixual_adjunct(parts):
    if len(parts) != 2:
        return False
    if parts[0][0] not in vowels or parts[1][0] in vowels:
        return False
    return True

def is_aspectual_adjunct(parts):
    if len(parts) != 1:
        return False
    if parts[0][0] not in vowels:
        return False
    return True

def is_bias_adjunct(parts):
    if len(parts) != 1:
        return False
    if parts[0][0] in vowels:
        return False
    return True

def split_word(s):
    if not s:
        return []
    elif s[0] in tones:
        return [s[0]] + split_word(s[1:])
    elif s[0] in consonants_s + [u'’', u'ʰ', u'-']:
        part = ''
        while s and s[0] in consonants_s + [u'’', u'ʰ', u'-']:
            part += s[0]
            s = s[1:]
        return [part] + split_word(s)
    elif s[0] in vowels + [u'’']:
        part = ''
        while s and s[0] in vowels + [u'’']:
            part += s[0]
            s = s[1:]
        return [part] + split_word(s)
    raise Exception('Something went terribly wrong')
    
def analyze_stress(parts):
    parts2 = parts[:]
    parts_no_stress = parts[:]
    
    for p in parts:
        if p[0] not in vowels and '-' not in p:
            parts2.remove(p)
            
    parts3 = []
    for p in parts2:
        parts4 = p.split(u'’')
        i = parts.index(p)
        for p4 in parts4:
            if p4: 
                if len(p4) == 2 and remove_accents(p4[1]) not in ('i','u'):
                    parts3.append((i, p4[0]))
                    parts3.append((i, p4[1]))
                elif len(p4) == 2 and p4[1] in grave_vowels:
                    parts3.append((i, p4[0]))
                    parts3.append((i, remove_accents(p4[1])))
                elif len(p4) == 2 and p4[1] in acute_vowels:
                    parts3.append((i, p4[0]))
                    parts3.append((i, p4[1]))
                elif len(p4) == 2 and p4[0] == p4[1]:
                    parts3.append((i, p4))
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
            if p[0] in (u'í', u'ú') and part.index(p[0]) > 0 and part[part.index(p[0])-1] in (u'a',u'e',u'i',u'o',u'u',u'ö',u'ë'):
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

def analyze_affixual_adjunct(parts):
    slots = {'type': 'Affixual adjunct', 1: (parts[0], parts[1])}
    return slots

def analyze_aspectual_adjunct(parts):
    slots = {'type': 'Aspectual adjunct', 1: parts[0]}
    return slots

def analyze_bias_adjunct(parts):
    slots = {'type': 'Bias adjunct', 1: parts[0]}
    return slots

def analyze_verbal_adjunct(parts):
    slots = {'type': 'Verbal adjunct'}
    
    if len(parts)>2 and parts[-2][-1] == u'’':
        parts[-2] = parts[-2][:-1]
        slots['G'] = parts[-1]
        parts = parts[:-1]
    
    if parts[-1][0] in vowels:
        slots['F'] = parts[-1]
        parts = parts[:-1]
        
    if parts[0] in tones:
        slots['H'] = parts[0]
        parts = parts[1:]
        
    slots['E'] = parts[-1]
    if len(parts) > 1:
        slots['D'] = parts[-2]
    if len(parts) > 2:
        slots['C'] = parts[-3]
    if len(parts) > 3:
        slots['B'] = parts[-4]
    if len(parts) > 4:
        slots['A'] = parts[-5]
    
    return slots

def analyze_personal_adjunct(parts):
    slots = {'type': 'Personal adjunct'}
    
    if parts[0] in tones:
        slots['tone'] = parts[0]
        parts = parts[1:]
        
    if parts[-1][0] not in vowels:
        slots['bias'] = parts[-1]
        parts[-2] = parts[-2][:-1]
        parts = parts[:-1]
        
    if parts[-2] in ('w', 'y', 'h', 'hw'):
        slots['Cz'] = parts[-2]
        slots['Vz'] = parts[-1]
        if parts[-3][-1] == u'’':
            parts[-3] = parts[-3][:-1]
            slots['Cz'] = u'’' + slots['Cz']
        parts = parts[:-2]
        
    slots['C1'] = parts[-2]
    slots['V1'] = parts[-1]
    parts = parts[:-2]
    
    if (len(slots['C1']) == 1 and slots['C1'] not in (u'g', u'd', u'j', u'ż', u'c', u'b')) or slots['C1'] == u'xh':
        #single-referent
        slots['CsVs'] = []
        if len(parts) == 1:
            slots['V2'] = parts[0]
        else:
            while parts:
                slots['CsVs'].append((parts[-1], parts[-2]))
                parts = parts[:-2]
    else:
        #dual-referent
        slots['Ck'] = slots['C1']
        del slots['C1']
        
        slots['V2'] = parts[-1]
        parts = parts[:-1]
        if parts:
            slots['C2'] = parts[-1]
            parts = parts[:-1]
        if parts:
            slots['Vw'] = parts[-1]
            
    return slots

def analyze_formative(parts):
    slots = {'type': 'Formative'}
    
    #first, we determine slots XII and XIII
    #tone
    if parts[0] in tones:
        slots[14] = parts[0]
        parts = parts[1:]
        
    #bias
    if parts[-2][-1] == u'’':
        slots[13] = parts[-1]
        parts[-2] = parts[-2][:-1]
        slots[12] = parts[-2]
        parts = parts[:-2]
        
    if parts[-1][0] in vowels:
        slots[12] = parts[-1]
        parts = parts[:-1]    
    #slots XII and XIII are now determined
    
    #now we determine if slots I-III are filled
    if parts[0][0] in vowels:
        if validation(parts[1]) or '-' in parts[1]:
            slots[2] = parts[0]
            slots[3] = parts[1]
            slots[4] = parts[2]
            parts = parts[3:]
        else:
            slots[4] = parts[0]
            parts = parts[1:]
    else:
        if validation(parts[0]) or '-' in parts[0]:
            slots[3] = parts[0]
            slots[4] = parts[1]
            parts = parts[2:]
        else:
            if '-' in parts[2]:
                slots[1] = parts[0]
                slots[2] = parts[1]
                slots[3] = parts[2]
                slots[4] = parts[3]
                parts = parts[4:]
    #now slots I-IV are determined and parts begin with slot V or VII     
        
    #are slots V and VI filled?
    #check format
    if 12 in slots and slots[12] not in ('a', 'i', 'e', 'u'):
        slots[5] = parts[0]
        slots[6] = parts[1]
        slots['type5'] = 'Cx'
        parts = parts[2:]
        
    #search for glottal stop:
    if 4 in slots and slots[4][-1] == u'’':
        if 5 not in slots:
            slots[5] = parts[0]
            slots[6] = parts[1]
            slots['type5'] = 'Cv'
            parts = parts[2:]
        slots[4] = slots[4][:-1]
    
    #if there was no glottal stop or format, check -wë-
    try:
        if 5 not in slots:
            for i in range(len(parts)):
                if parts[i] == 'w' and parts[i+1] == u'ë' and i != 2:
                    slots[5] = parts[0]
                    slots[6] = parts[1]
                    slots['type5'] = 'Cv'
                    parts = parts[2:]
                    break
    except:
        pass
    
    #now slots V and VII are determined and we are at slot VII
            
    slots[7] = parts[0]
    slots[8] = parts[1]
    parts = parts[2:]
    #now we know slots VII and VIII
    
    if u'’' in slots[8] and slots[8][-1] != u'’':
        #handle xx'V case
        pts = slots[8].split(u'’')
        if pts[1] != u'a' or 4 not in slots:
            slots[4] = pts[1]
        elif pts[1] != u'a' and 4 in slots:
            raise Exception('wtf')
        slots[8] = pts[0] + u'’V'
    
    if parts[0] in ('w', 'y', 'h', 'hw'):
        if parts[0] == 'hw' and len(slots[8]) > 1 and slots[8][-1] == 'i' and slots[8][-2] != u'’':
            slots[9] = 'y' + parts[1]
        elif parts[0] == 'hw' and slots[8] in (u'a',u'e',u'i',u'o',u'ö',u'ë'):
            slots[9] = 'w' + parts[1]
            slots[8] = slots[8] + 'u'
        else:
            slots[9] = parts[0] + parts[1]
        parts = parts[2:]
        
    slots[10] = parts[0]
    parts = parts[1:]
    
    slots[11] = []
    while parts:
        slots[11].append((parts[0], parts[1]))
        parts = parts[2:]
    
    if 4 not in slots:
        slots[4] = 'a'
    
    return slots
    
def analyze_word(word):
    word = unicode(word)
    word = word.replace('\'', u'’')
    
    parts_stress = split_word(word.lower())
    stress, parts = analyze_stress(parts_stress)
    
    if is_bias_adjunct(parts):
        slots = analyze_bias_adjunct(parts)
        
    elif is_aspectual_adjunct(parts):
        slots = analyze_aspectual_adjunct(parts)
    
    elif is_verbal_adjunct(parts):
        slots = analyze_verbal_adjunct(parts)
        
    elif is_affixual_adjunct(parts):
        slots = analyze_affixual_adjunct(parts)
    
    elif is_personal_adjunct(parts):
        slots = analyze_personal_adjunct(parts)
        slots['stress'] = stress
    
    else:
        slots = analyze_formative(parts)
        slots['stress'] = stress
        
    return slots
