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

from Declare4Py.ProcessMiningTasks.QueryChecking.DeclareQueryChecker import DeclareQueryChecker
from Declare4Py.ProcessMiningTasks.QueryChecking.DeclareResultsBrowser import DeclareResultsBrowser



"""
    Minimal working Example for Model Discovery involving the Declare Miner.

    This shows how to do perform a discovery of Declare model and then how to save the model as a .decl file. 

    It uses the DeclareMiner class.
"""

# This class has the Declare Miner. 
from Declare4Py.ProcessMiningTasks.Discovery.DeclareMiner import DeclareMiner

# Load an event log to work with. 
RawFile = os.path.join("testLogs/SepsisCases.xes")

# Create the Declare4Py EventLog.
SepsisLog: D4PyEventLog = D4PyEventLog(case_name="case:concept:name")

# Initialize the EventLog with the data. 
SepsisLog.parse_xes_log(RawFile)

# The Discovery of a Declare Model require that the DeclareMiner gets instantiated with some parameters.
    # log - It takes the regular event log.
    # consider_vacuity - True or False. It treats vacuously satisfied traces as satisfied, or violated otherwise.
    # min_support - Sets the minimum support of how much of the log has to be satisfied by EACH discovered constraint.
    # itemsets_support - Sets a fraction of how often a set of 2 activities in a Trace should be added as an candidate for Discovery of an constraint.
    # max_declare_cardinality - Sets the amount of activities a declare constraint can have. {1,2,3}.

discovery : DeclareMiner= DeclareMiner(log=SepsisLog,
                         consider_vacuity=False,
                         min_support=0.2,
                         itemsets_support=0.9,
                         max_declare_cardinality=3)
discoveryModel: DeclareModel = discovery.run()
print(discoveryModel.serialized_constraints)

