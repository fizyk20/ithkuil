ithkuil
=======

A Python package providing tools for analysing texts in the [Ithkuil](http://ithkuil.net) constructed language.

## Features

- Parsing of Ithkuil formatives and adjuncts into morphemes - defined by a PEG in _ithkuil.parser.grammar_
- Unit tests checking the correctness of the parser
- An SQLite database containing morphological and grammatical data - the relations between morphemes and grammatical categories
(ithkuil/morphology/morphology.db)
- _test.py - a test script: morphological analysis of some example words
- gloss_sentence.py - a script performing the glossing of the text given via command line or standard input

There is also a keyboard layout making it possible to type special characters being used in Ithkuil.
It has been moved to a separate repository - [ithkuil-utils](https://github.com/fizyk20/ithkuil-utils)

## TODOs

Near future:

- Encode the sentence grammar in the PEG
- Update the grammar to take into account the changes made after November 2014
- Improve the grammar to accomodate mathematical expressions
- ~~Complete the database - include morphemes for adjuncts (current version only has formatives)~~

Far future:

- Word composer module: specify the values of the grammatical categories and get the word back
- Add a module for generation of images with Ithkuil native writing from latin

Would be awesome, but not sure if feasible:

- OCR for conversion of native writing into latin transcription
