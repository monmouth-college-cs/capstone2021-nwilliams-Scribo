# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 19:07:23 2021

@author: Nate


This a little demonstration of what I was doing to incorporate scientific/mathematical
fields into Classics with

Models trained with data from the Perseus Ancient Greek and Latin Dependency Treebanks v2.0 by 
Giuseppe G. A. Celano, Gregory Crane, Bridget Almas & al.. Copyright Perseus Digital Library, Tufts University, 2014.
Licensed under a CC BY-SA 3.0 license. http://perseusdl.github.io/treebank_data/.
"""

import pickle as pkl
import tkinter as tk

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
          } #24 is a dummy value representing where a word doesn't have a character

models = []
with open("storedmodels.pkl", "rb") as file:
    while True:
        try:
            models.append(pkl.load(file))
        except EOFError:
            break
        
#print(models)

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
inp = tk.Entry(frame)
inp.pack()
prediction = tk.Label(frame)
prediction.pack()
checkButton = tk.Button(frame, text="Check it!", command = lambda: makePrediction())
checkButton.pack()

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

vPerDict = {0 : '-', #for participles
            1 : '1',
            2 : '2',
            3 : '3'}

vNumDict = {0 : '-', #for participles
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

def makePrediction():
    tokens = inp.get().split()
    for i in range(len(tokens)):
        tokens[i].lower()
    data = []
    for r in range(len(tokens)):
        temp = [24] * 28
        tempcount = 0
        for t in range(len(tokens[r])):
            temp[tempcount] = letters[tokens[r][t]]
            tempcount = tempcount + 1
        data.append(temp)
        
    predictions = []
    for i in range(len(data)):
        pos = postargetdic[models[0].predict([data[i]])[0]]
        person = vPerDict[models[5].predict([data[i]])[0]]
        num = "-"
        if ((pos == 'n') or (pos == 'a')):
                num = number[models[1].predict([data[i]])[0]]
        elif (pos == 'v'):
                num = vNumDict[models[6].predict([data[i]])[0]]
        tense = vTenseDict[models[7].predict([data[i]])[0]]
        mood = vMoodDict[models[8].predict([data[i]])[0]]
        voice = voice = vVoiceDict[models[8].predict([data[i]])[0]]
        gen = gender[models[2].predict([data[i]])[0]]
        cas = case[models[3].predict([data[i]])[0]]
        deg = "-"
        predictions.append(pos + person + num + tense + mood + voice + gen + cas + deg)
    temp = ""
    for i in range(len(predictions)):
        temp = temp + " " + predictions[i]
    prediction.config(text = temp)
    
root.mainloop()