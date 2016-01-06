import pytest
from ithkuil.parser import parseWord

words_to_test = [
    ('aukkras', -2),
    ('quit', -2),
    ('/qʰûl-lyai’svukšei’arpîptó’ks', -1)
]

@pytest.mark.parametrize('word, expected', words_to_test)  
def test_stress(word, expected):
    parsedWord = parseWord(word)
    assert parsedWord['stress'] == expected