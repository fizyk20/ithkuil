import pytest
from ithkuil.parser import parseWord

words_to_test = [
    
    ('hruštrul-lyö’ň', {
        'type': 'verbal adjunct',
        'tone': None,
        'Cl': 'hr',
        'Ve': 'u',
        'Cv': 'štr',
        'Vm': 'u',
        'Cs': 'l-ly',
        'Vs': 'ö',
        'Cb': 'ň'
    }),
                 
    ('wëtöin-n', {
        'type': 'verbal adjunct',
        'tone': None,
        'Cl': 'w',
        'Ve': 'ë',
        'Cv': 't',
        'Vm': 'öi',
        'Cs': 'n-n',
        'Vs': None,
        'Cb': None
    }),
                 
    ('hëtiun-n', {
        'type': 'verbal adjunct',
        'tone': None,
        'Cl': 'h',
        'Ve': 'ë',
        'Cv': 't',
        'Vm': 'iu',
        'Cs': 'n-n',
        'Vs': None,
        'Cb': None
    }),
                 
    ('on-n', {
        'type': 'verbal adjunct',
        'tone': None,
        'Cl': None,
        'Ve': None,
        'Cv': None,
        'Vm': 'o',
        'Cs': 'n-n',
        'Vs': None,
        'Cb': None
    }),
                 
    ('ur-rwu', {
        'type': 'verbal adjunct',
        'tone': None,
        'Cl': None,
        'Ve': None,
        'Cv': None,
        'Vm': 'u',
        'Cs': 'r-rw',
        'Vs': 'u',
        'Cb': None
    }),
                 
    ('ulan-n', {
        'type': 'verbal adjunct',
        'tone': None,
        'Cl': None,
        'Ve': 'u',
        'Cv': 'l',
        'Vm': 'a',
        'Cs': 'n-n',
        'Vs': None,
        'Cb': None
    }),
                 
    ('pal-lši', {
        'type': 'verbal adjunct',
        'tone': None,
        'Cl': None,
        'Ve': None,
        'Cv': 'p',
        'Vm': 'a',
        'Cs': 'l-lš',
        'Vs': 'i',
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
