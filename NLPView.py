# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 12:10:49 2021

@author: Nate
"""

import tkinter as tk

class View:
    #Main window junk
    root = tk.Tk()
    rootMenu = tk.Menu(root)
    content = tk.Frame(root)
    
    #Or else the debil will show up on run
    root.withdraw()
    
    #other stuff
    sentText = "Hello! Click the 'Generate a new sentence' button to get started."
    sentence = tk.Label(root, textvar= sentText)
    userInput = tk.Entry(root)
    expectedPOS = "The POStags you should get will appear here when you generate a new sentence."
    expectedText = tk.Label(root, textvar = expectedPOS)
    
    #Init
    def __init__(self):
        self.root = tk.Tk()
        self.content = tk.Frame(self.root)
        self.rootMenu = tk.Menu(self.root)
        self.makeMenus()
        self.sentence = tk.Label(self.root, text="Hello!")
        self.userInput = tk.Entry(self.root)
        self.sentence.pack()
        self.userInput.pack()
        self.expectedText.pack()
    
    #Auxiliary methods
    def makeMenus(self):
        #Program Menu
        self.progMenu = tk.Menu(self.rootMenu, tearoff=0)
        self.progMenu.add_command(label="Exit", command= lambda: self.root.quit())
        self.rootMenu.add_cascade(label="Program", menu= self.progMenu)
    
        #Nouns and Adjectives Menu
        naMenu = tk.Menu(self.rootMenu, tearoff=0)
        naMenu.add_command(label="Case", command= lambda: self.lesson("ncase"))
        naMenu.add_command(label="Gender and Number", command=lambda: self.lesson("ngendernumber"))
        naMenu.add_command(label="Declension", command= lambda: self.lesson("declension"))
        naMenu.add_command(label="Degree", command= lambda: self.lesson("adjdegree"))
        self.rootMenu.add_cascade(label="Nouns and Adjectives", menu=naMenu)
        
        #Verbs
        vMenu = tk.Menu(self.rootMenu, tearoff=0)
        vMenu.add_command(label="Number and Person", command= lambda: self.lesson("numper"))
        vMenu.add_command(label="Conjugation", command= lambda: self.lesson("conj"))
        vMenu.add_command(label="Tense", command= lambda: self.lesson("tense"))
        vMenu.add_command(label="Voice", command= lambda: self.lesson("voice"))
        vMenu.add_command(label="Mood", command= lambda: self.lesson("mood"))
        
        #Adverbs
        advMenu = tk.Menu(self.rootMenu, tearoff=0)
        advMenu.add_command(label="Degree", command= lambda: self.lesson("advdegree"))
    
    def start(self):
        self.root.mainloop()
    
    def lesson(self, lesson):
        if lesson == "ncase":
            self.case()
        elif lesson == "ngendernumber":
            self.gennumb()
        elif lesson == "declension":
            self.declension()
        elif lesson == "adjdegree":
            self.adjdegree()
        elif lesson == "numper":
            self.numper()
        elif lesson == "conj":
            self.conj()
        elif lesson == "tense":
            self.tense()
        elif lesson == "voice":
            self.voice()
        elif lesson == "mood":
            self.mood()
        elif lesson == "advdegree":
            self.advdegree()
            
    
    def case(self):
        tk.messagebox.showinfo("Case", """
                               Latin has 7 cases, which are ways that nouns and adjectives function and are formed. Adjectives should always have the same case as their complement (the noun they modify).
                               
                               Here are the cases!
                               Nominative: 
                                   Used for the subjects of sentences and for complements for linking verbs (like est)
                               Genitive: 
                                   Used for possession, usually, but there are other uses, like partitive genitives.
                               Dative: 
                                   Used for indirect objects and prepositions.
                               Accusative: 
                                   Used for direct objects and prepositions.
                               Ablative: 
                                   Used to describe how verbs are done (like when, where, by whom, with what), prepositions, and a whole sleu of other things.
                               Vocative: 
                                   Used for directly addressing someone/something.
                               Locative: 
                                   A special case that only works with certain nouns. Used instead of prepostions, denoting that something is at or to the noun.
                               """)
        
    def gennumb(self):
        tk.messagebox.showinfo("Gender and Number", """
                               Nouns and adjectives in Latin have gender and number. Genders are masculine, feminine, or neuter. Most of the time, a declension can determine gender (i.e. 1st is typically feminine, 2nd is typically masculine or neuter). Gender need not be literal. Number is simply whether there is one (singular) or many (plural).""")
       
    def declension(self):
        tk.messagebox.showinfo("Declension", "pretend there's a chart here.")
        
    def adjdegree(self):
        tk.messagebox.showinfo("Adjective Degree",
                               """Adjectives in Latin come in three degrees, describing how 'intense' the adjective is:
                                  Positive: Uses either first, second, or third declension endings, used as a baseline intensity
                                  Comparative: Uses third declension endings with -ior, used for comparison or when describing something as being 'rather adjectivey'
                                  Superlative: Uses first and second declension endings with -issimus or -rrimus, used when describing the highest intensity
                                  """)
            
    def numper(self):
        tk.messagebox.showinfo("Number and Person",
                               """
                               Like nouns and adjectives, verbs have the two standard numbers: singular and plural.
                               Verbs also have person, describing the generic subject of the verb: 1st for when oneself is the subject, 2nd for when
                               someone one is addressing is the subject, and 3rd for when someone or something not directly addressed is the subject.
                               """)
    
    def conj(self):
        tk.messagebox.showinfo("Conjugation",
                               """"
                               There are 4 declensions of verbs: 
                               1st (which are -o, -are), 
                               2nd (-eo, -ere), 3rd (-o, -ere), 
                               3rd-io (-io, -ere), 
                               and 4th (-io, -ire)
                               """)
    
    def tense(self):
        tk.messagebox.showinfo("Tenses",
                               """
                               Latin verbs use 6 tenses:
                               Present: Formed with present stem and personal endings,
                               Imperfect: ongoing actions began in the past, formed with present stem,
                               Perfect: completed actions in the past, formed with perfect stem,
                               Pluperfect: actions completed before other completed actions in the past, formed with perfect stem,
                               Future: formed with present stem,
                               and Future Perfect: completed actions in the future, formed with perfect stem
                               """)
            
    def voice(self):
        tk.messagebox.showinfo("Voice",
                               """
                               Latin verbs are either active or passive. Acitive is used when the subject is acting,
                               Passive is used when the subject is being acted upon.
                               """)
    def mood(self):
        tk.messagebox.showinfo("Mood",
                               """
                               Verbs have one of these moves:
                               Indicative: Simple Verbs,
                               Infinitive: A fancy way of saying 'to verb', used as a verbal noun,
                               Imperative: Commands,
                               Participle: A verbal adjective,
                               Subjunctive: 'Less real' verbs,
                               Gerund: A verbal noun,
                               Gerundive: Another form of verbal adjective, specifically future passive participle,
                               Supine: Another verbal noun, referring to the actual act
                               """)
            
    def advdegree(self):
        tk.messagebox.showinfo("Adverb Degree",
                               """
                               Like adjectives, adverbs have degree. Unlike adjectives, adverbs are not declineable.
                               Standard entry for positive,
                               -iter for comparative,
                               -issime or -rrime for superlative.
                               """)