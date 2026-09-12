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
    Minimal Working Example for Query Checking of 
    Declare checker. 

    Shows how to query check a DECLARE constraint in a log 
    and how to browse the results. 
"""

# The DeclareQueryChecker class takes some input.
    # * An event log. 
    # * Bool for Consider_vacuity, it essentially implies that
    # trivial satisfied traces are considered as satisfied. 
    # Violated other wise.
    # * Some query settings. Sets the DECLARE constraint and the 
    # Variables to ask. I a parameter is not set then it is treated
    # as a variable to ask. 
    # * min_support=float sets support to be satisfied in the log
    # by the variable assignments. 
    # * return first=bool, false returns all the variables assignments 
    # that satisfies the support in the log. Otherwise, it returns
    # only one variables assignment, that support the log. Saves 
    # time and computing time. IF one is only interested in the 
    # existence of a variable assignment with a given support. 

RawLog = os.path.join("testLogs/SepsisCases.xes")
SepsisLog: D4PyEventLog = D4PyEventLog()
SepsisLog.parse_xes_log(RawLog)

# We initiate the DeclareQueryChecker object wit all the parameters.
query_checker = DeclareQueryChecker(log=SepsisLog, consider_vacuity=False, template='Chain Response', activation='IV Antibiotics', activation_condition='A.org:group is A', min_support=0.2, return_first=False)

# We begin to find the variable assignments that satisfies the constraint given above. 
query_check_res: DeclareResultsBrowser = query_checker.run()

# Print the result as a table. 
print(query_check_res.filter_query_checking(queries=['template', 'activation', 'target', 'activation_condition']).to_string())

# I found that QueryChecking is used to help figure out what events are needed to complete a the constraint. Activation can activate a constraint, and then query checking is used to find what target/ other events is needed to satisfy the constraint. 

# To find this you need min_support and that essentially says how much % of the logs traces a constraint has to be satisfied for. 
    # For our 1050 traces, a min_support of 20 % would result in 210 traces. This implies that if a candidate target wants to be accepted, the target event has to work in at least 210 traces of the log. 

    # In our example we check the Chain response constraint where IV Antibotics are the activation of the constraint. Activation need org:group = A, and the rule needs at least 20 % support in the log. Since we have return_first, we say that we want all the targets that satisfies the constraint. This means that our output has found 5 different constraints combinations that satisfies 20 % of the log. 

    # In previous MWE:s, we have looked at conformance checking, essentially, checking if our traces in the logs follow some predefined model. 

    # In Query Checking we want to find events/variables that could create a rule together with another event/variable. I think this is closly connected to what we want to do, since this seems like it has to do with the creation of a constraints Model. 

    # Lets look at another example.

print("-------- New Example --------")

# We do another query checking, but now for the template Response, with a higher support as well. 
# IMPORTANT, this time we don't have an activation event, and therefore the QueryChecker has to figure out which events that can be an activation and which events can be the target event. The constraint that is being implemented are Response. 
query_checker = DeclareQueryChecker(log=SepsisLog, consider_vacuity=False, template='Response', min_support=0.8, return_first=False)

# Start the query checker. 
query_check_res: DeclareResultsBrowser = query_checker.run()

# Print the result.
print(query_check_res.filter_query_checking(queries=['template', 'activation', 'target']).to_string())