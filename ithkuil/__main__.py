#!/usr/bin/env python

from .morphology import fromString
    
print('Type \'quit\' to quit.')
while True:
    text = input('Type a sentence: ')
    if text == 'quit':
        break
    words = text.split()
    for word in words:
        if not word: continue
        print('%s: %s' % (word, fromString(word).abbreviatedDescription()))
