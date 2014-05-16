#!/usr/bin/env python

from morphology import Word

print('Formatives:\n')

words = ['/qʰûl-lyai’svukšei’arpîptó’ks', '¯uhmixhákc’', 'eglelôn', 'ükšàwëla', 
         'Ükšoàwîl', 'pal', 'užapqaušš', 'Iùltawâlüšq' ]
    
for word in words:
    print(word, ': ', Word.fromString(word).slots)
    
print('\nPersonal adjuncts:\n')

words = ['mrerîwa’ks', 'ˇxhoehwe', 'këi', 'êti', 'uhiaksai’wé’ks', 'Awuçkʰoewi']
    
for word in words:
    print(word, ': ', Word.fromString(word).slots)
    
print('\nVerbal:\n')

words = ['hruštrul-lyö’ň']
    
for word in words:
    print(word, ': ', Word.fromString(word).slots)
    
print('\nAffixual:\n')

words = ['ar', 'eirţ']
    
for word in words:
    print(word, ': ', Word.fromString(word).slots)
    
sentence = 'Aukkras  êqutta  ogvëuļa  tnou’elkwa  pal-lši  augwaikštülnàmbu'
words = sentence.split()
    
print('\n%s:\n' % sentence)
    
for word in words:
    print(word, ': ', Word.fromString(word).slots)
    
sentence = 'Ükʰu attál în-n uhednaláň'
words = sentence.split()
    
print('\n%s:\n' % sentence)
    
for word in words:
    print(word, ': ', Word.fromString(word).slots)
