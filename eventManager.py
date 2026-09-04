import warnings
import os

# This class is responsible for managing .xes files event logs.
from Declare4Py.D4PyEventLog import D4PyEventLog

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

warnings.filterwarnings("ignore", category=UserWarning)

# This is how the event log is instantiated. 
event_log: D4PyEventLog = D4PyEventLog(case_name="case:concept:name")

# Save the path to the event log in a variable.
log_path = os.path.join("testLogs/repair_example(500 traces).xes")

# Parse and convert the log file into the event_log class variable. 
event_log.parse_xes_log(log_path)

##############
# Print the parsed log
# Case == Trace.
# Concept:name == Event name.
##############

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

# Print the .xes file in a readable fashion.
print_less(event_log)