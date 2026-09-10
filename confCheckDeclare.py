import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import os

# This class is responsible for managing .xes files event logs.
from Declare4Py.D4PyEventLog import D4PyEventLog

# Library for managing process models 
# The models are created wit LTL -> Linear Temporal Logic
from Declare4Py.ProcessModels.LTLModel import LTLModel # This is a class. 

from Declare4Py.ProcessModels.LTLModel import LTLTemplate

from Declare4Py.ProcessModels.DeclareModel import DeclareModel

from Declare4Py.ProcessModels.DeclareModel import DeclareModelTemplate

# This can handle Linear Temporal Logic Strings and parse them 
from ltlf2dfa.parser.ltlf import LTLfParser

# LTLAnalyzer makes it possible to check our traces in the log to evaluate its conformance. 
from Declare4Py.ProcessMiningTasks.ConformanceChecking.LTLAnalyzer import LTLAnalyzer

# These classes initializes the DECLARE conformance checking.
from Declare4Py.ProcessMiningTasks.ConformanceChecking.MPDeclareAnalyzer import MPDeclareAnalyzer
from Declare4Py.ProcessMiningTasks.ConformanceChecking.MPDeclareResultsBrowser import MPDeclareResultsBrowser


"""
    Minimal Working Example for Coformance checking with a Declare Model. 

    We are using DeclareModel and DeclareModelTemplate. In previous MWE's, we used LTLModel and LTLTemplate
"""

# Create the EventLog Obejct.
RawLog = os.path.join("testLogs/SepsisCases.xes")
SepsisLog = D4PyEventLog(case_name="case:concept:name")
SepsisLog.parse_xes_log(RawLog)

# Create the DeclareModel Object. 
rawModel = os.path.join("testLogs/data_model.decl")
declareModel = DeclareModel().parse_from_file(rawModel)

# We retrieve the constraints of the model
modelConstraints = declareModel.get_decl_model_constraints()

# This prints all the Declare constraints in the .decl file.
#print("Model Constraints:")
#print("-----------------")
#for idx, constr in enumerate(modelConstraints):
#    print(idx, constr)


# This initializes the DECLARE analyzer. 
# Consider vacuity if True can assume trivial satisfied traces are considered True.
# Declare4Py has implemented some sort of MP Declare Analyzer algorithm.
basicChecker = MPDeclareAnalyzer(log=SepsisLog, declare_model=declareModel, consider_vacuity=False)

# Now Run will start to check if the Log's traces are conforming. 
confCheckRes: MPDeclareResultsBrowser = basicChecker.run()

# The result of the run method is a ResultsBrowser object.
# get_metric() can be used to retrieve conformance checking results. It takes the metrix parameter with values in num_pendings, num_activations, num_fulfillments, num_violations and state.
print(confCheckRes.get_metric(trace_id=1, metric="num_activations"))

# The prints are a table with rows that are the results of each trace according to the DECLARE constraints in the model. Each Column in the table represents the DECLARE constraints in the model. 