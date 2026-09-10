import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import os

# This class is responsible for managing .xes files event logs.
from Declare4Py.D4PyEventLog import D4PyEventLog

# Library for managing process models 
# The models are created wit LTL -> Linear Temporal Logic
from Declare4Py.ProcessModels.LTLModel import LTLModel # Thiss is a class. 

from Declare4Py.ProcessModels.LTLModel import LTLTemplate

from Declare4Py.ProcessModels.DeclareModel import DeclareModel

from Declare4Py.ProcessModels.DeclareModel import DeclareModelTemplate

# This can handle Linear Temporal Logic Strings and parse them 
from ltlf2dfa.parser.ltlf import LTLfParser

# LTLAnalyzer makes it possible to check our traces in the log to evaluate its conformance. 
from Declare4Py.ProcessMiningTasks.ConformanceChecking.LTLAnalyzer import LTLAnalyzer

"""
    Minimal Working Example to check if a event log follows the constraints set by a LTLf Model. 

    The Minimal working example uses the LTLf Syntax, LTLf Templates and Target-Branched Declare Templates. 
"""

# Load a raw .xes file to test Conformance of.
LogRaw = os.path.join("testLogs/SepsisCases.xes")

# Create the Declare EventLog and parse the log.
SepsisLog = D4PyEventLog()

# Should be 1050 Traces.
SepsisLog.parse_xes_log(LogRaw)

# Let's create a LTLf Model.  
model = LTLModel()

# We give the Model a very simple constraint.
# Eventually C Will Release P. 
model.parse_from_string("F(CRP)")

# Instantiate the Analyzer.
analyzer = LTLAnalyzer(SepsisLog, model)

# The run method does the conformance checking by transforming the model into a DFA and then checks if a trace is accepted by the DFA. 
conf_check_res_df = analyzer.run() # VERY Important. There is some sort of bug involving jobs > 1. Set the defult. 
print(conf_check_res_df.to_string())


# We do another example with LTLf Templates instead of parse from string.
template: LTLTemplate = LTLTemplate('eventually_a')

# Create a model with the template-filler function.
# CRP is a variable name. 
model2: LTLModel = template.fill_template(['CRP'])

print(model2.formula)

analyzer = LTLAnalyzer(SepsisLog, model2)
resultDF = analyzer.run()

# Prints everything, we see that False indicates that a trace didnot have a CRP event in its trace. True, indicates at least one occurance of CRP in its trace.  
#print(resultDF.to_string())

# There is a lot of examples using these templates. But #Now we are going to look at the declare models instead #of LTLf Models. 

# This is a Declare constraint 
template = LTLTemplate('precedence')

# Activities to fill the precedence with. 
activities_a = ["ER Triage", "CRP"]
activities_b = ["Leucocytes", "Admission NC", "Resease A"]

# Fill the template.
model = template.fill_template(activities_a, activities_b)
analyzer = LTLAnalyzer(SepsisLog, model)
resDF = analyzer.run()
print(resDF.to_string())
print(f"Formula: {model.formula}\n")


# It is also possible to query the resulting pandas dataframes. We do so below. 

# This querys the output and checks how many traces have an conforming trace.
print(f"Accepted traces: {len(resDF[resDF['accepted'] == True])}") 

