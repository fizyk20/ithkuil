import pytest
from ithkuil.parser import parseWord

words_to_test = [
    
    ('hruštrul-lyö’ň', {
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
        'tone': None,
        'Cl': None,
        'Ve': 'u',
        'Cv': 'l',
        'Vm': 'a',
        'Cs': 'n-n',
        'Vs': None,
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
