import pytest
from ithkuil.parser import parseWord

words_to_test = [
    
    ('ou', {
        'type': 'aspectual adjunct',
        'Vs': 'ou'
    }),
    
    ('ui', {
        'type': 'aspectual adjunct',
        'Vs': 'ui'
    }),
    
    ('ar', {
        'type': 'affixual adjunct',
        'VxC': { 'type': 'r', 'degree': 'a' }
    }),
    
    ('eirţ', {
        'type': 'affixual adjunct',
        'VxC': { 'type': 'rţ', 'degree': 'ei' }
    }),
    
    ('ss', {
        'type': 'bias adjunct',
        'Cb': 's',
        'Cb+': True
    }),
    
    ('çç', {
        'type': 'bias adjunct',
        'Cb': 'ç',
        'Cb+': True
    }),
    
    ('kšš', {
        'type': 'bias adjunct',
        'Cb': 'kš',
        'Cb+': True
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
