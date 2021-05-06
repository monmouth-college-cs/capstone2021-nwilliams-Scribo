# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:26:59 2021

@author: Nate

Models trained with data from the Perseus Ancient Greek and Latin Dependency Treebanks v2.0 by 
Giuseppe G. A. Celano, Gregory Crane, Bridget Almas & al.. Copyright Perseus Digital Library, Tufts University, 2014.
Licensed under a CC BY-SA 3.0 license. http://perseusdl.github.io/treebank_data/.
"""

import NLPModel
import NLPView
import NLPController

Model = NLPModel.Model()
View = NLPView.View()
Controller = NLPController.Controller(View, Model)

View.start()