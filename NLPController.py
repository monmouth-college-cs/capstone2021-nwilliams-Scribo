# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 23:04:54 2021

@author: Nate
"""

import tkinter as tk
import NLPModel as mod
import NLPView as vew

class Controller:
    model = mod.Model()
    view = vew.View()
    root = view.root
    CheckButton = tk.Button()
    NewButton = tk.Button()
    
    def __init__(self, View, Model):
        self.model = Model
        self.view = View
        self.CheckButton = tk.Button(self.view.root, text = "Check your translation!", command= lambda: self.model.makePrediction(self.view.userInput.get()))
        self.NewButton = tk.Button(self.view.root, text = "Generate a new sentence", command= lambda: self.generate())
        self.CheckButton.pack()
        self.NewButton.pack()
        
    def generate(self):
        self.model.generateSentence()
        self.view.sentText = self.model.translations[self.model.totrans]
        self.view.expectedPOS = self.model.expected[self.model.totrans]