# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:16:17 2021

@author: Nate

Models trained with data from the Perseus Ancient Greek and Latin Dependency Treebanks v2.0 by 
Giuseppe G. A. Celano, Gregory Crane, Bridget Almas & al.. Copyright Perseus Digital Library, Tufts University, 2014.
Licensed under a CC BY-SA 3.0 license. http://perseusdl.github.io/treebank_data/.
"""

import pickle as pkl
import random as rdm


class Model:
    #fields

    #Curated translations
    translations = {
            0 : 'Marcus picks up the dog.',
            1 : 'The rock was rather small.',
            2 : 'Anna will run swiftly.',
            3 : 'The biggest rocks had been given to the king.'
            }
    
    #Order in Perseus: PoS, Person, Number, Tense, Mood, Voice, Gender, Case, Degree
    expected = {
            0 : ["n-s---mn-", "v3spia---", "n-s---ma-"],
            1 : ["n-s---nn-", "v3sria---", "a-s---nnc"],
            2 : ["n-s---fn-", "v3sfia---", "d--------"],
            3 : ["n-p---nn-", "a-p---nn-", "v3plip---"]
            }
    
    #Strings to/from view
    userstring = ""
    generatedstring = ""
    totrans = 0
    
    #Formatting and Prediction dictionaries
    letters = {'a': 0,
          'b': 1,
          'c': 2,
          'd': 3,
          'e': 4,
          'f': 5,
          'g': 6,
          'h': 7,
          'i': 8,
          'k': 9,
          'l': 10,
          'm': 11,
          'n': 12,
          'o': 13,
          'p': 14,
          'q': 15,
          'r': 16,
          's': 17,
          't': 18,
          'u': 19,
          'v': 20,
          'x': 21,
          'y': 22,
          'z': 23
          }
    
    postargetdic = {
        0 : 'n', #nouns
 		1 : 'v', #verbs
 		2 : 't', #participles?
 		3 : 'a', #adjectives
 		4 : 'd', #adverbs
 		5 : 'c', #conjunctions
 		6 : 'r', #prepositions
 		7 : 'p', #pronoun
 		8 : 'm', #numeral
 		9 : 'i', #interjection
 		10 : 'e', #exclamation
 		11 : 'u', #punctuation
        12 : '-'} #I have literally no clue

    number = {0 : 's', #singular
              1 : 'p'} #plural
    
    case = {0 : 'n', #nom
            1 : 'g', #gen
            2 : 'd', #dat
            3 : 'a', #acc
            4 : 'b', #abl
            5 : 'v', #voc
            6 : 'l'} #loc
    
    gender = {0 : 'm', #masc
              1 : 'f', #fem
              2 : 'n'} #neut
    
    adjdeg = {'-' : 0,
              'c' : 1,
              's' : 2}
    
    vPerDict = {0 : '-', #for participles
                1 : '1',
                2 : '2',
                3 : '3'}
    
    vNumDict = {0 : '-',
                1 : 's',
                2: 'p'
                }
    
    vTenseDict = {0 : 'p', #pres
                  1 : 'i', #impf
                  2 : 'r', #prf
                  3 : 'l', #plu
                  4 : 't',#futprf
                  5 : 'f' #fut
                  }
    
    vMoodDict = {0 : 'i',
                 1 : 's',
                 2 : 'n',
                 3 : 'm',
                 4 : 'p',
                 5 : 'd',
                 6 : 'g',
                 7 : 'u'
                 }

    vVoiceDict = {0 : 'a',
                  1 : 'p',
                  2 : 'd'}
    
    
    #models(experimental)
    models = []
    with open("storedmodels.pkl", "rb") as file:
        while True:
            try:
                models.append(pkl.load(file))
            except EOFError:
                break
    
    #methods
    
    #Init
    def __init__(self):
        self.generateSentence()
    
    #Predictions
    def makePrediction(self, inp):
        self.userstring = inp
        tokens = self.userstring.split()
        for i in range(len(tokens)):
            tokens[i].lower()
        data = []
        for r in range(len(tokens)):
            temp = [24] * 28
        tempcount = 0
        for t in range(len(tokens[r])):
            temp[tempcount] = self.letters[tokens[r][t]]
            tempcount = tempcount + 1
        data.append(temp)
        
        predictions = []
        for i in range(len(data)):
            pos = self.postargetdic[self.models[0].predict([data[i]])[0]] #everything should have a POS
            person = "-"
            num = "-"
            tense = "-"
            mood = "-"
            voice = "-"
            gen = "-"
            cas = "-"
            deg = "-"
        if ((pos == 'n') or (pos == 'a')):
                num = self.number[self.models[1].predict([data[i]])[0]]
                gen = self.gender[self.models[2].predict([data[i]])[0]]
                cas = self.case[self.models[3].predict([data[i]])[0]]
                if pos == 'a':
                    deg = self.adjdeg[self.models[4].predict([data[i]])[0]]
        elif (pos == 'v'):
                num = self.vNumDict[self.models[6].predict([data[i]])[0]]
                person = self.vPerDict[self.models[5].predict([data[i]])[0]]
                tense = self.vTenseDict[self.models[7].predict([data[i]])[0]]
                mood = self.vMoodDict[self.models[8].predict([data[i]])[0]]
                voice = self.vVoiceDict[self.models[8].predict([data[i]])[0]]
                if person == "-":                                           #participles can be treated as adjectives
                    gen = self.gender[self.models[2].predict([data[i]])[0]]
                    cas = self.case[self.models[3].predict([data[i]])[0]]
        elif pos == 'd':
            pass
                    
        predictions.append(pos + person + num + tense + mood + voice + gen + cas + deg)
        temp = ""
        for i in range(len(predictions)):
            temp = temp + " " + predictions[i]
        self.generatedstring = temp
    
    #Other Run-Time                            
    def updateInput(self, new):
        self.userstring = new
        
    def generateSentence(self):
        self.totrans = rdm.randint(0, len(self.translations) -1 )
        