#!/usr/bin/env python

from morphology import Word
    
if __name__ == '__main__':
    print('Type \'quit\' to quit.')
    while True:
        text = input('Type a sentence: ')
        if text == 'quit':
            break
        words = text.split()
        for word in words:
            if not word: continue
            print('%s: %s' % (word, Word.fromString(word).describe()))
