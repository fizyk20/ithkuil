#!/usr/bin/env python

from word_splitter import analyze_word

print('Formatives:\n')

words = ['/qʰûl-lyai’svukšei’arpîptó’ks', '¯uhmixhákc’', 'eglelôn', 'ükšàwëla', 
         'Ükšoàwîl', 'pal', 'užapqaušš', 'Iùltawâlüšq' ]
    
for word in words:
    print(word, ': ', analyze_word(word))
    
print('\nPersonal adjuncts:\n')

words = ['mrerîwa’ks', 'ˇxhoehwe', 'këi', 'êti', 'uhiaksai’wé’ks', 'Awuçkʰoewi']
    
for word in words:
    print(word, ': ', analyze_word(word))
    
print('\nVerbal:\n')

words = ['hruštrul-lyö’ň']
    
for word in words:
    print(word, ': ', analyze_word(word))
    
print('\nAffixual:\n')

words = ['ar', 'eirţ']
    
for word in words:
    print(word, ': ', analyze_word(word))
    
sentence = 'Aukkras  êqutta  ogvëuļa  tnou’elkwa  pal-lši  augwaikštülnàmbu'
words = sentence.split()
    
print('\n%s:\n' % sentence)
    
for word in words:
    print(word, ': ', analyze_word(word))
    
sentence = 'Ükʰu attál în-n uhednaláň'
words = sentence.split()
    
print('\n%s:\n' % sentence)
    
for word in words:
    print(word, ': ', analyze_word(word))
