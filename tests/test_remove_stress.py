import pytest
from ithkuil.morphology.words import remove_stress

txts_to_test = [
    ('a', 'a'),
    ('o', 'o'),
    ('áu', 'au'),
    ('ái', 'ai'),
    ('aú', 'aù'),
    ('aé', 'ae'),
    ('á', 'a')
]

@pytest.mark.parametrize('txt, expected', txts_to_test)
def test_word(txt, expected):
    assert remove_stress(txt) == expected