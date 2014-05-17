#!/usr/bin/env python

from morphology import fromString

print('Formatives:\n')

words = ['/qʰûl-lyai’svukšei’arpîptó’ks', '¯uhmixhákc’', 'eglelôn', 'ükšàwëla', 
         'Ükšoàwîl', 'pal', 'užapqaušš', 'Iùltawâlüšq' ]
    
for word in words:
    print(word, ': ', fromString(word).abbreviatedDescription())
    
print('\nPersonal adjuncts:\n')

words = ['mrerîwa’ks', 'ˇxhoehwe', 'këi', 'êti', 'uhiaksai’wé’ks', 'Awuçkʰoewi']
    
for word in words:
    print(word, ': ', fromString(word).abbreviatedDescription())
    
print('\nVerbal:\n')

words = ['hruštrul-lyö’ň']
    
for word in words:
    print(word, ': ', fromString(word).abbreviatedDescription())
    
print('\nAffixual:\n')

words = ['ar', 'eirţ']
    
for word in words:
    print(word, ': ', fromString(word).abbreviatedDescription())
    
sentence = 'Aukkras  êqutta  ogvëuļa  tnou’elkwa  pal-lši  augwaikštülnàmbu'
words = sentence.split()
    
print('\n%s:\n' % sentence)
    
for word in words:
    print(word, ': ', fromString(word).abbreviatedDescription())
    
sentence = 'Ükʰu attál în-n uhednaláň'
words = sentence.split()
    
print('\n%s:\n' % sentence)
    
for word in words:
    print(word, ': ', fromString(word).abbreviatedDescription())
