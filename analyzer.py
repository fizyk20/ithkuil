#!/usr/bin/env python

from word_splitter import analyze_word

slot_dicts = {}

def init():
    for i in list(range(1,15)) + ['stress']:
        slot_dicts[i] = {}
        try:
            with open('data/slot%s.dat' % i, 'r') as f:
                for line in f:
                    line = line.replace('\n','')
                    pts = line.split(': ')
                    slot_dicts[i][pts[1]] = pts[0]
            if i == 11:
                with open('data/slot11deg.dat', 'r') as f:
                    for line in f:
                        line = line.replace('\n','')
                        pts = line.split(': ')
                        slot_dicts[i][pts[1]] = pts[0]
        except:
            pass

def describe_formative(slots):
    desc = []
    for i in list(range(1,15)) + ['stress']:
        if i in slots:
            try:
                if i == 7:
                    desc.append(str(slots[i]))
                    continue
                if i != 11:
                    desc.append(slot_dicts[i][slots[i]])
                else:
                    for suf in slots[11]:
                        desc.append('%s_%s' % (slot_dicts[i][suf[1]], slot_dicts[i][suf[0]]))
            except:
                print('No entry found for slot %s: %s' % (i, slots[i]))
    return '-'.join(desc)

def describe(word):
    slots = analyze_word(word)
    
    if slots['type'] == 'formative':
        return describe_formative(slots)
    
    else:
        return 'TODO'
    
if __name__ == '__main__':
    init()
    word = ''
    while word != 'quit':
        word = input('Type a word: ')
        print(describe(word))