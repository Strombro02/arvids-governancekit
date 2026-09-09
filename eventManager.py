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

def ltlfExamples():
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
    print(f"Formula (Added Negation !): {model.formula}")

    # This adds the implication after the formula. Therefore, the new implication will be to the right of the old fomula.
    model.add_implication("F(Release A)")
    print(f"Fomrula (Added Negation Implication): {model.formula}")

    print("--------------------\n")

    model.parse_from_string("Leucocytes")
    print(f"Start Formula: \n {model.formula}")

    # New operator U = Until. This says that the previous formula has to be true until the new formula occurs. It differs from Release since the later fomrula has to occur, for the entire formula to be true. <a a a> is not true if we have (a U b), but it is true if we have (a R b). 
    # It adds the input formula to the end of the other formula.
    model.add_until("!(CRP)")
    print(f"Formula (Added Until): \n {model.formula}")

    # Added an always to the beginning of the fomula. 
    model.add_always()
    print(f"Formula (Added G): \n {model.formula}")

    print("--------------------\n")
    # New example
    model.parse_from_string("IV Liquid")
    print(f"Start Formula: \n {model.formula}")

    # Adds OR to the model, adds this to the end of the fomula.
    model.add_disjunction("IV Antibiotics")
    print(f"Formula (Added OR): \n {model.formula}")

    # Adds AND to the model with an new formula expression. 
    # X == Next. And the fomula says that Admission NC as the next event is allowed. "AND Next Admission NC is allowed allowed in the trace."  
    model.add_conjunction("X[!](Admission NC)")
    print(f"Formula (Added AND): \n {model.formula}")

    print("--------------------\n")

    # New example
    model.parse_from_string("Return ER")
    print(f"Start Formula: \n {model.formula}")

    # Adds next infront.
    model.add_next()
    print(f"Formula (Added Next): \n {model.formula}")

    # Equivalance added after the original formula.
    model.add_equivalence("Bad condition")
    print(f"Formula (Added <=>): \n {model.formula}")

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

# Checking LTLf model satisfiability
# There is a method called check_satisfiability, which uses the Lydia backend to transform the LTLf models to a DFA. 

# Declare4Py offers two methods to switch backends to either Lydia or LTLf 

model = LTLModel()

model.parse_from_string("CRP & X[!](F(ER Triage && X[!](F(Admission NC))))")

# This will check if the model formula is satisfiable. Expected True.
print(f"{model.formula} is satisfiable? {model.check_satisfiability()}")

# F = Eventually, F(a) a has to occur some time later. Expected False.
# By default Lydia is used as backend to convert LTLf fomrula into DFA.
# Default Declare4Py -> Lydia -> DFA (Satisfiability = Does a trace exists that satisfies the formula?)
# Declare4Py -> LTLf2DFA -> DFA.  
# Switch Between Backends LTLf2DFA or Lydia with model.to_lydia_backend() or model.to_ltlf2dfa_backend()
model.parse_from_string("G(CRP) && F(!(CRP))")

# Minimize will minimize the outputting DFA before satisfiability is performed.
print(f"{model.formula} is satisfiable? {model.check_satisfiability(minimize_automaton=True)}")

############# A LTLTemplate class ############
# Templates may be used to more easiliy fill LTL rules. First you state which template to use then th .fill_template() mehtod may be used to fill the template. 

template = LTLTemplate('eventually_a_then_b')
model = template.fill_template(['Leucocytes', 'CRP'])

# a then b is represented vid AND since b has to directly follow a. 
print(f"Formula for {template.template_str}:  {model.formula}")



# DeclareModel and DeclareModelTemplate
# We can get both unary and binary templates by using the following

# These will simply store the templates that is allowed. 
unary_templates = DeclareModelTemplate.get_unary_templates()
binary_templates = DeclareModelTemplate.get_binary_templates()

# Parsing of a DECLARE model. 
ModelPath = os.path.join("testLogs/data_model.decl")

# Creates a DeclareModel from a file containing Declare Constraints. The file contains the model itself, which are Activities and Constraints/Relationships.

# data_model.decl starts the process rules where Existance2 is. Then Chain seems to add constraints to the model after.
# This is a declare model and not a LTLModel. Therefore, it can not be printable later, since 
model = DeclareModel().parse_from_file(ModelPath)

# We check if the model from data_model.decl is satisfiable.
print(f"Declare Model from File: {model.formula} ")



# Get all the activities and constraints from the Declare Model
modelActivities = model.get_model_activities()
modelConstraints = model.get_decl_model_constraints()

# Prints all the activities and the constraints. 
print("Model activities:")
print("-----------------")
for idx, act in enumerate(modelActivities):
    print(idx, act)
print("\n")

print("Model constraints:")
print("-----------------")
for idx, constr in enumerate(modelConstraints):
    print(idx, constr)





