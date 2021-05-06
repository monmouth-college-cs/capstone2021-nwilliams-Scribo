# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:36:46 2021

@author: Nate


Models trained with data from the Perseus Ancient Greek and Latin Dependency Treebanks v2.0 by 
Giuseppe G. A. Celano, Gregory Crane, Bridget Almas & al.. Copyright Perseus Digital Library, Tufts University, 2014.
Licensed under a CC BY-SA 3.0 license. http://perseusdl.github.io/treebank_data/.
"""
#Data
import xml.etree.ElementTree as et #for reading the xml files, which compose the PT
import os #for getting the xml files
import pandas as pd
import pickle as pkl

#Machine Learning
from sklearn.tree import DecisionTreeClassifier
#from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
#from sklearn.preprocessing import LabelEncoder, OneHotEncoder Proved not great
from sklearn.metrics import make_scorer, precision_score, f1_score

pkl_filename = "storedmodels.pkl"
models = []

treebanks = os.listdir('./Perseus Treebanks')

forms = [] #The word itself
postags = [] #The word's grammar

#Get data from Perseus Treebanks
parsecounter = 1

for m in range(len(treebanks)):
    doc = et.parse('./Perseus Treebanks' + '/' + treebanks[m])
    root = doc.getroot()
    
    for sents in root:
        for words in sents:
            f = words.get('form')
            p = words.get('postag')
            if (((f == None) or (p == None)) or (not f.isalpha()) or (p == '')):
                pass
            else:
                forms = forms + [f]
                postags = postags + [p]
    print('%s' %parsecounter)
    parsecounter = parsecounter + 1    
#print(forms[0:10])
#print(postags[0:10])
    
#postags are arranged as such:
# part of speech, person, number, mood,

#Standardize how forms are written
#See if macronizer would help
#One might argue that u and v should be combined, but I will not
#as they are not combined in most learning material
for i in range(len(forms)):
    temp = forms[i]
    forms[i] = temp.lower()
    for j in range(len(temp)):
        if temp[j] == 'j':
            forms[i][j] = 'i'

print(forms[0:10])

#Prepare POS Targets            
#pos = {}
counter = 0
postargetdic = {
        'n'	: 0, #nouns
 		'v'	: 1, #verbs
 		't'	: 2, #participles?
 		'a'	: 3, #adjectives
 		'd'	: 4, #adverbs
 		'c'	: 5, #conjunctions
 		'r'	: 6, #prepositions
 		'p'	: 7, #pronoun
 		'm'	: 8, #numeral
 		'i'	: 9, #interjection
 		'e'	: 10, #exclamation
 		'u'	: 11, #punctuation
        '-' : 12} #I have literally no clue
#for l in postags:
 #   if not(l[0] in pos.keys()):
  #      pos.update({l[0] : counter})
   #     counter = counter + 1
    #else:
     #   pass
        
#print(pos)

postarget = []

for z in range(len(postags)):
#    postarget.append(pos[postags[z][0]])
    postarget.append(postargetdic[postags[z][0]])
    
#print(postarget[0:10])

#Prepare Forms
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

OHEletters = {0: 'a',
          1: 'b',
          2: 'c',
          3: 'd',
          4: 'e',
          5: 'f',
          6: 'g',
          7: 'h',
          8: 'i',
          9: 'k',
          10: 'l',
          11: 'm',
          12: 'n',
          13: 'o',
          14: 'p',
          15: 'q',
          16: 'r',
          17: 's',
          18: 't',
          19: 'u',
          20: 'v',
          21: 'x',
          22: 'y',
          23: 'z',
          24: '-'
          } #24 is a dummy value representing where a word doesn't have a character

posdata = [None] * len(forms)
forwardposdata = [None] * len(forms)

#I'll try a "forward facing" letter order as well, to see how it compares to the idea below
for r in range(len(forms)):
    temp = [24] * 28
    tempcount = 0
    for t in range(len(forms[r])):
        temp[tempcount] = letters[forms[r][t]]
        tempcount = tempcount + 1
    forwardposdata[r] = temp

#print(forwardposdata[0:10])

#The idea of arranging the words such that they are backwards comes from this:
#The endings of words tend to either sole or predominant determiner of the word's
#grammar. Thus, in order for models to make better connections between ending letters
#which would otherwise have variable positions, the order of letters is backwards, making their
#position less variable.
for r in range(len(forms)):
    temp = [24] * 28 #allegedly, the longest Latin word ever is 28 characters long
    tempcount = 0
    t = len(forms[r]) - 1
    while t >= 0:
        temp[tempcount] = letters[forms[r][t]]
        tempcount = tempcount + 1
        t = t - 1
    posdata[r] = temp     


#for one hot encoding
OHEForms = [None] * len(posdata)

for i in range(len(posdata)):
    temp = ['-'] * 28
    tempcount = 0
    for t in range(len(posdata[i])):
        temp[tempcount] = OHEletters[posdata[i][t]]
        tempcount = tempcount + 1
    OHEForms[i] = temp
    
print(OHEForms[0:10])
#print(posdata[0:10])

#print(len(posdata))


#prepare data for model training
X_train, X_test, y_train, y_test = train_test_split(posdata, postarget)

#forward_X_train, forward_X_test, forward_y_train, forward_y_test = train_test_split(forwardposdata, postarget)

gs = GridSearchCV(DecisionTreeClassifier(),
                  param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                                cv = 3)
                                
gs.fit(X_train, y_train)
print('\n Backward Decision Tree results:')
print(gs.best_score_)
models.append(gs.best_estimator_)
print("Model[0] is pos")
print('\n')

#fgs = GridSearchCV(DecisionTreeClassifier(),
 #                   param_grid = {'max_depth' : (None, 5, 10),
 #                               'min_samples_split': (2, 3, 4, 5, 10)})

#fgs.fit(forward_X_train, forward_y_train)

#print('Forward Decision Tree results:')
#print(fgs.best_score_)

#rfgs = GridSearchCV(RandomForestClassifier(),
#                    param_grid = {'n_estimators': (10, 50, 100)})

#rfgs.fit(X_train, y_train)
#print('\n Random Forest results:')
#print(fgs.best_params_)
#print(fgs.best_score_)

degree = {'-' : 0,
          'c' : 1,
          's' : 2}

#get nouns and adjectives
nounForms = []
adjectiveData = []
nounPostags = []
adjectivePostags = []
bothData = []
bothPostags = []
for i in range(len(postags)):
    if ((postags[i][2].isalpha()) and (postags[i][6].isalpha()) and (postags[i][7].isalpha())):
        bothData = bothData + [posdata[i]]
        bothPostags = bothPostags + [postags[i]]
        if postags[i][0] == 'n':
            nounForms = nounForms + [posdata[i]]
            nounPostags = nounPostags + [postags[i]]
        elif ((postags[i][0] == 'a') and (postags[i][8] in degree.keys())):
                adjectiveData = adjectiveData + [posdata[i]]
                adjectivePostags = adjectivePostags + [postags[i]]
        else:
            pass
    else:
        pass
    
print(nounPostags[0:10])
print(adjectivePostags[0:10])

number = {'s' : 0,
          'p' : 1}

case = {'n' : 0,
        'g' : 1,
        'd' : 2,
        'a' : 3,
        'b' : 4,
        'v' : 5,
        'l' : 6} #for indeclinable nouns like nihil or fas

gender = {'m' : 0,
          'f' : 1,
          'n' : 2}

nounadjNum = [None] * len(bothPostags)
nounadjCase = [None] * len(bothPostags)
nounadjGen = [None] * len(bothPostags)

bothDataFrame = pd.DataFrame(bothData)
bothForms = pd.get_dummies(bothDataFrame).values

adjectiveDataFrame = pd.DataFrame(adjectiveData)
adjectiveForms = pd.get_dummies(adjectiveDataFrame).values

for i in range(len(bothPostags)):
    nounadjNum[i] = number[bothPostags[i][2]]
    nounadjCase[i] = case[bothPostags[i][7]]
    nounadjGen[i] = gender[bothPostags[i][6]]

adjDeg = [None] * len(adjectivePostags)

for i in range(len(adjectivePostags)):
    adjDeg[i] = degree[adjectivePostags[i][8]]
    
number_X_train, number_X_test, number_y_train, number_y_test = train_test_split(bothForms, nounadjNum)

gender_X_train, gender_X_test, gender_y_train, gender_y_test = train_test_split(bothForms, nounadjGen)

case_X_train, case_X_test, case_y_train, case_y_test = train_test_split(bothForms, nounadjCase)

deg_X_train, deg_X_test, deg_y_train, deg_y_test = train_test_split(adjectiveForms, adjDeg)

num_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)

num_gscv.fit(number_X_train, number_y_train)
print('Number results (knn):')
print(num_gscv.best_score_)
print(num_gscv.best_params_)
models.append(num_gscv.best_estimator_)
print("Models[1] is noun numbers")

gen_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)

gen_gscv.fit(gender_X_train, gender_y_train)
print('Gender results (knn):')
print(gen_gscv.best_score_)
print(gen_gscv.best_params_)

gender_dt_gscv = GridSearchCV(DecisionTreeClassifier(),
                             param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                                           cv = 3)
    
gender_dt_gscv.fit(gender_X_train, gender_y_train)
print('Gender results (dt):')
print(gender_dt_gscv.best_score_)
models.append(gender_dt_gscv.best_estimator_)
print("Models[2] is gender")

case_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)

case_gscv.fit(case_X_train, case_y_train)
print('Case results (knn):')
print(case_gscv.best_score_)
print(case_gscv.best_params_)

case_dt_gscv = GridSearchCV(DecisionTreeClassifier(),
                             param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                                           cv = 3)
    
case_dt_gscv.fit(case_X_train, case_y_train)
print('Case results (dt):')
print(case_dt_gscv.best_score_)
models.append(case_dt_gscv.best_estimator_)
print("Models[3] is case")

deg_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)

deg_gscv.fit(deg_X_train, deg_y_train)
print('Degree results (knn):')
print(deg_gscv.best_score_)
print(deg_gscv.best_params_)
models.append(deg_gscv.best_estimator_)
print("Models[4] is degree")

#VERBS, for participles, apply appropriate predictors here and from Nouns/Adjectives
#I'll try encoding here
verbForms = []
verbTags = []
for i in range(len(postags)):
    if postags[i][0] == 'v':
        verbForms = verbForms + [posdata[i]]
        verbTags = verbTags + [postags[i]]
        
print(len(verbForms) == len(verbTags))



verbPerson = []
verbNumber = []
verbTense = []
verbMood = []
verbVoice = []
verbData = []
verbFrameData = []

vPerDict = {'-': 0, #for participles
            '1': 1,
            '2': 2,
            '3': 3}

vNumDict = {'-': 0, #for participles
            's': 1,
            'p': 2
            }

vTenseDict = {'p': 0,
              'i': 1,
              'r': 2,
              'l': 3,
              't': 4,
              'f': 5
              }

vMoodDict = {'i': 0,
             's': 1,
             'n': 2,
             'm': 3,
             'p': 4,
             'd': 5,
             'g': 6,
             'u': 7
             }

vVoiceDict = {'a': 0,
              'p': 1,
              'd': 2}

for i in range(len(verbTags)):
    if (verbTags[i][1] in vPerDict):
        if (verbTags[i][2] in vNumDict):
            if(verbTags[i][3] in vTenseDict):
                if(verbTags[i][4] in vMoodDict):
                    if(verbTags[i][5] in vVoiceDict):
                        verbPerson = verbPerson + [vPerDict[verbTags[i][1]]]
                        verbNumber = verbNumber + [vNumDict[verbTags[i][2]]]
                        verbTense = verbTense + [vTenseDict[verbTags[i][3]]]
                        verbMood = verbMood + [vMoodDict[verbTags[i][4]]]
                        verbVoice = verbVoice + [vVoiceDict[verbTags[i][5]]]
                        verbData = verbData + [verbForms[i]]

#verbDataFrame = pd.DataFrame(verbFrameData)
#verbData = pd.get_dummies(verbDataFrame).values
#vPersonEncoder = LabelEncoder()
#vPersonTargets = vPersonEncoder.fit_transform(verbPerson)
#
#vNumberEncoder = LabelEncoder()
#vNumberTargets = vNumberEncoder.fit_transform(verbNumber)
#
#vTenseEncoder = LabelEncoder()
#vTenseTargets = vTenseEncoder.fit_transform(verbTense)
#
#vMoodEncoder = LabelEncoder()
#vMoodTargets = vMoodEncoder.fit_transform(verbMood)
#
#vVoiceEncoder = LabelEncoder()
#vVoiceTargets = vVoiceEncoder.fit_transform(verbVoice)

vPerson_X_train, vPerson_X_test, vPerson_y_train, vPerson_y_test = train_test_split(verbData, verbPerson)
vNumber_X_train, vNumber_X_test, vNumber_y_train, vNumber_y_test = train_test_split(verbData, verbNumber)
vTense_X_train, vTense_X_test, vTense_y_train, vTense_y_test = train_test_split(verbData, verbTense)
vMood_X_train, vMood_X_test, vMood_y_train, vMood_y_test = train_test_split(verbData, verbMood)
vVoice_X_train, vVoice_X_test, vVoice_y_train, vVoice_y_test = train_test_split(verbData, verbVoice)

scores = {'accuracy': 'accuracy',
          'precision': make_scorer(precision_score, average = 'macro'),
          'f1_score': make_scorer(f1_score, average = 'macro')}

vperson_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        scoring = scores,
                        refit = 'f1_score',
                        cv = 3)
vperson_gscv.fit(vPerson_X_train, vPerson_y_train)
print('Verb Person results (knn):')
print(vperson_gscv.best_score_)
#print(vperson_gscv.cv_results_)
print(vperson_gscv.best_params_)

vperson_gscvDT = GridSearchCV(DecisionTreeClassifier(), 
                        param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                        scoring = scores,
                        refit = 'f1_score',
                        cv = 3)
vperson_gscvDT.fit(vPerson_X_train, vPerson_y_train)
print('Verb Person results (DT):')
print(vperson_gscvDT.best_score_)
#print(vperson_gscvDT.cv_results_)
print(vperson_gscvDT.best_params_)
models.append(vperson_gscvDT.best_estimator_)
print("Models[5] is person") 

vnumber_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)
vnumber_gscv.fit(vNumber_X_train, vNumber_y_train)
print('Verb Number results (knn):')
print(vnumber_gscv.best_score_)
print(vnumber_gscv.best_params_)

vnumber_gscvDT = GridSearchCV(DecisionTreeClassifier(), 
                        param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                        cv = 3)
vnumber_gscvDT.fit(vNumber_X_train, vNumber_y_train)
print('Verb Number results (DT):')
print(vnumber_gscvDT.best_score_)
print(vnumber_gscvDT.best_params_)
models.append(vnumber_gscvDT.best_estimator_)
print("Models[6] is verb number")

vtense_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)
vtense_gscv.fit(vTense_X_train, vTense_y_train)
print('Verb Tense results (knn):')
print(vtense_gscv.best_score_)
print(vtense_gscv.best_params_)

vtense_gscvDT = GridSearchCV(DecisionTreeClassifier(), 
                        param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                        scoring = scores,
                        refit = 'f1_score',
                        cv = 3)
vtense_gscvDT.fit(vTense_X_train, vTense_y_train)
print('Verb Tense results (DT):')
print(vtense_gscvDT.best_score_)
print(vtense_gscvDT.best_params_)
models.append(vtense_gscvDT.best_estimator_)
print("Models[7] is tense")

#For comparison
vtense_nonCV = DecisionTreeClassifier()
vtense_nonCV.set_params(**vtense_gscvDT.best_params_)


vmood_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)
vmood_gscv.fit(vMood_X_train, vMood_y_train)
print('Verb Mood results (knn):')
print(vmood_gscv.best_score_)
print(vmood_gscv.best_params_)

vmood_gscvDT = GridSearchCV(DecisionTreeClassifier(), 
                        param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                        cv = 3)
vmood_gscvDT.fit(vMood_X_train, vMood_y_train)
print('Verb Mood results (DT):')
print(vmood_gscvDT.best_score_)
print(vmood_gscvDT.best_params_)
models.append(vmood_gscvDT.best_estimator_)
print("Models[8] is mood")

vvoice_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)
vvoice_gscv.fit(vVoice_X_train, vVoice_y_train)
print('Verb Voice results (knn):')
print(vvoice_gscv.best_score_)
print(vvoice_gscv.best_params_)

vvoice_gscvDT = GridSearchCV(DecisionTreeClassifier(), 
                        param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                        cv = 3)
vvoice_gscvDT.fit(vVoice_X_train, vVoice_y_train)
print('Verb Voice results (DT):')
print(vvoice_gscvDT.best_score_)
print(vvoice_gscvDT.best_params_)
models.append(vvoice_gscvDT.best_estimator_)
print("Models[9] is voice")

#Adverbs
adverbForms = []
adverbTags = []
for i in range(len(postags)):
    if postags[i][0] == 'd':
        adverbForms = adverbForms + [posdata[i]]
        adverbTags = adverbTags + [postags[i]]

advDegree = {'-' : 0,
             'c' : 1,
             's' : 2}

adverbData = []
adverbTargets = []

for i in range(len(adverbTags)):
    if adverbTags[i][8] in advDegree:
        adverbData = adverbData + [adverbForms[i]]
        adverbTargets = adverbTargets + [advDegree[adverbTags[i][8]]]
        
advDeg_X_train, advDeg_X_test, advDeg_y_train, advDeg_y_test = train_test_split(adverbData, adverbTargets)

advDeg_gscv = GridSearchCV(KNeighborsClassifier(), 
                        param_grid = {'n_neighbors' : range(1, 10)},
                        cv = 3)

advDeg_gscv.fit(advDeg_X_train, advDeg_y_train)
print('Adverb Degree (KNN):')
print(advDeg_gscv.best_params_)
print(advDeg_gscv.best_score_)

advDeg_gscvDT = GridSearchCV(DecisionTreeClassifier(), 
                        param_grid = {'max_depth' : range(1, 10),
                                      'min_samples_leaf' : range(1, 10),
                                      'min_samples_split': range(2,10)},
                        cv = 3)

advDeg_gscvDT.fit(advDeg_X_train, advDeg_y_train)
print('Adverb Degree (DT):')
print(advDeg_gscvDT.best_params_)
print(advDeg_gscvDT.best_score_)
        
with open(pkl_filename, "wb") as file:
   for model in models:
        pkl.dump(model, file)