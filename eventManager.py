import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import os

# This class is responsible for managing .xes files event logs.
from Declare4Py.D4PyEventLog import D4PyEventLog

# Library for managing process models 
# The models are created wit LTL -> Linear Temporal Logic
from Declare4Py.ProcessModels.LTLModel import LTLModel # Thiss is a class. 

# This can handle Linear Temporal Logic Strings and parse them 
from ltlf2dfa.parser.ltlf import LTLfParser

def print_less(event_log: D4PyEventLog):
    """
        Prints all cases but with limited information.
        Prints it in a readable way.
        Timestamt | Resource | Event
    """

    for case in event_log.get_log():
        case_id = case.attributes["concept:name"]

        print(f"\nCase: {case_id}")
        print("-" * 40)

        for event in case:
            print(
                f'{event["time:timestamp"]} | '
                f'{event["org:resource"]:10} | '
                f'{event["concept:name"]}'
            )

def printLogInformation():
    print_less(event_log)

    print("This is the log:")
    print(event_log.get_log())
    print("--------------------------------------")

    # Print the number of cases in the log
    print("Number of cases:")
    print(event_log.get_length())
    print("--------------------------------------")

    # Print the number of cases in the log
    print("Case name:")
    print(event_log.get_case_name())
    print("--------------------------------------")

    # Print the number of cases in the log
    print("Concept name:")
    print(event_log.get_concept_name())
    print("--------------------------------------")

    # Print the number of cases in the log
    print("Timestamp name:")
    print(event_log.get_timestamp_name())


warnings.filterwarnings("ignore", category=UserWarning)

# This is how the event log is instantiated. 
event_log: D4PyEventLog = D4PyEventLog(case_name="case:concept:name")

# Save the path to the event log in a variable.
log_path = os.path.join("testLogs/repair_example(500 traces).xes")

# Parse and convert the log file into the event_log class variable. 
event_log.parse_xes_log(log_path)

# Instatiate the Linear Temporal Logic Model.
# The model contains an attribute: formula that stores the formula as a string 
model = LTLModel()

# They use the LTLf syntax found 
# "Always(E Release Triage (implicerar) Eventually (C Release  P))"
model.parse_from_string("G(ER Triage -> F(CRP))")

# Create the parser for LTLf syntax.
parser = LTLfParser()

# Alltid/Globally (a (implicerar -> ) WeakNext b)
# Om a händer, då ska b hända i nästa steg OM det finns ett steg till.  
formulaStr = "G(a -> WX b)"

# This returns a LTLf formula object
formulaObj = parser(formulaStr)

# Prints the formula with the LTLf syntax. 
# print(formulaObj)

##############
# We can do other logical operations on the formulas with 
# the LTLModel class. 
# Some Examples
##############

# This takes a formula String and saves it within the model.
# C Release P.
# It seems more or less that the model contains a Long string of Linear Temporal Logic. And the Model has methods to add to the formula string.
# R == Release it says that P has to be true up until C. The Trace: <P P P P C X Y Z > Is true since C releases the obligations of P when C is true. However, before C is true, nothing except P may be true.
model.parse_from_string("C R P") 
print(f"Start Formula: {model.formula}")

# Adds an eventually at the front of the formula.
model.add_eventually()
print(f"Formula (Added Eventually F): {model.formula}")

# We add a negation to the beginning of the string.
model.add_negation()
print(f"Fomrula (Added Negation !): {model.formula}")

# This adds the implication after the formula. Therefore, the new implication will be to the right of the old fomula.
model.add_implication("F(Release A)")
print(f"Fomrula (Added Negation Implication): {model.formula}")

print("--------------------\n")

model.parse_from_string("Leucocytes")
print(f"Formula: \n {model.formula}")

# New operator U = Until
model.add_until("!(CRP)")
print(f"Fomrula (Added Util): \n {model.formula}")

