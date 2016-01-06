import pytest
from ithkuil.parser import parseWord

words_to_test = [
    
    ('poi', {
        'type': 'personal adjunct',
        'tone': None,
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
        'tone': '¯',
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
        'tone': None,
        'C1': 't',
        'Vc': 'eu',
        'Cz': 'y',
        'Vz': 'e',
        'VxC': [{ 'type': 'f', 'degree': 'o' }],
        'Vc2': None,
        'Vw': None,
        'C2': None,
        'Ck': None,
        'Cb': 'çç'
    }),
    
    ('epoi', {
        'type': 'personal adjunct',
        'tone': None,
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
    })

]

@pytest.mark.parametrize('word, expected', words_to_test)  
def test_word(word, expected):
    parsedWord = parseWord(word)
    for key in expected:
        if not expected[key]:
            assert key not in parsedWord
        else:
            assert parsedWord[key] == expected[key]
