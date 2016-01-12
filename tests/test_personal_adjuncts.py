import pytest
from ithkuil.parser import parseWord

words_to_test = [

    ('poi', {
        'type': 'personal adjunct',
        '[tone]': None,
        '[stress]': -2,
        'C1': 'p',
        'Vc': 'oi',
        'Cz': None,
        'Vz': None,
        'VxC': None,
        'Vc2': None,
        'Vw': None,
        'C2': None,
        'Ck': None,
        'Cb': None
    }),

    ('¯tiwu', {
        'type': 'personal adjunct',
        '[tone]': '¯',
        '[stress]': -2,
        'C1': 't',
        'Vc': 'i',
        'Cz': 'w',
        'Vz': 'u',
        'VxC': None,
        'Vc2': None,
        'Vw': None,
        'C2': None,
        'Ck': None,
        'Cb': None
    }),

    ('foteuye’çç', {
        'type': 'personal adjunct',
        '[tone]': None,
        '[stress]': -2,
        'C1': 't',
        'Vc': 'eu',
        'Cz': 'y',
        'Vz': 'e',
        'VxC': [{ 'type': 'f', 'degree': 'o' }],
        'Vc2': None,
        'Vw': None,
        'C2': None,
        'Ck': None,
        'Cb': 'ç',
        'Cb+': True
    }),

    ('epoi', {
        'type': 'personal adjunct',
        '[tone]': None,
        '[stress]': -2,
        'C1': 'p',
        'Vc': 'oi',
        'Cz': None,
        'Vz': None,
        'VxC': None,
        'Vc2': 'e',
        'Vw': None,
        'C2': None,
        'Ck': None,
        'Cb': None
    }),

    ('_uda', {
        'type': 'personal adjunct',
        '[tone]': '_',
        '[stress]': -2,
        'C1': None,
        'Vc': 'a',
        'Cz': None,
        'Vz': None,
        'VxC': None,
        'Vc2': 'u',
        'Vw': None,
        'C2': None,
        'Ck': 'd',
        'Cb': None
    }),

    ('awuçkʰoewi', {
        'type': 'personal adjunct',
        '[tone]': None,
        '[stress]': -2,
        'C1': None,
        'Vc': 'oe',
        'Cz': 'w',
        'Vz': 'i',
        'VxC': None,
        'Vc2': 'u',
        'Vw': 'a',
        'C2': 'w',
        'Ck': 'çkʰ',
        'Cb': None
    }),

    ('uhiaksai’wé’ks', {
        'type': 'personal adjunct',
        '[tone]': None,
        '[stress]': -1,
        'C1': None,
        'Vc': 'ai',
        'Cz': '’w',
        'Vz': 'é',
        'VxC': None,
        'Vc2': 'ia',
        'Vw': 'u',
        'C2': 'h',
        'Ck': 'ks',
        'Cb': 'ks',
        'Cb+': False
    }),

    ('ˇxhoehwe', {
        'type': 'personal adjunct',
        '[tone]': 'ˇ',
        '[stress]': -2,
        'C1': 'xh',
        'Vc': 'oe',
        'Cz': 'hw',
        'Vz': 'e',
        'VxC': None,
        'Vc2': None,
        'Vw': None,
        'C2': None,
        'Ck': None,
        'Cb': None
    }),

    ('mrerîwa', {
        'type': 'personal adjunct',
        '[tone]': None,
        '[stress]': -2,
        'C1': 'r',
        'Vc': 'î',
        'Cz': 'w',
        'Vz': 'a',
        'VxC': [{ 'type': 'mr', 'degree': 'e' }],
        'Vc2': None,
        'Vw': None,
        'C2': None,
        'Ck': None,
        'Cb': None
    })

]

@pytest.mark.parametrize('word, expected', words_to_test)
def test_word(word, expected):
    parsedWord = parseWord(word)
    for key in expected:
        if expected[key] is None:
            assert key not in parsedWord
        else:
            assert parsedWord[key] == expected[key]
