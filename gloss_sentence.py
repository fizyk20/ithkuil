#!/usr/bin/env python
from ithkuil.morphology.words import Factory
from ithkuil.morphology.exceptions import IthkuilException
import sys

words = sys.argv[1:]

if not words:
    words = sys.stdin.read().split()

for word in words:
    try:
        wordObj = Factory.parseWord(word)
        print(wordObj.word, ':', wordObj.abbreviatedDescription())
    except IthkuilException as e:
        print(word, ': ERROR: %s', str(e))

