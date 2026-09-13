import warnings

warnings.filterwarnings("ignore", category=UserWarning)


from Declare4Py.D4PyEventLog import D4PyEventLog
from Declare4Py.ProcessModels.DeclareModel import DeclareModel
from Declare4Py.ProcessMiningTasks.ConformanceChecking.MPDeclareAnalyzer import MPDeclareAnalyzer, MPDeclareResultsBrowser


# ==================================================
# GOVERNANCE RULE
# ==================================================
#
# Response[book_ticket, pay]
#
# Meaning:
# If book_ticket happens, pay must happen afterwards.
#
# ==================================================


# Load event log
event_log = D4PyEventLog(case_name="concept:name")
event_log.parse_xes_log("simple_log.xes")


# Load DECLARE model
declare_model = DeclareModel().parse_from_file("simple_model.decl")

# Run governance checking
checker = MPDeclareAnalyzer(
    log=event_log,
    declare_model=declare_model,
    consider_vacuity=False
)

results: MPDeclareResultsBrowser = checker.run()

states = results.get_metric(metric="state")

print("\n=== GOVERNANCE RESULTS ===\n")

for case_number, state in enumerate(states.iloc[:, 0], start=1):

    if state == 1:
        print(f"Case {case_number}: COMPLIANT")
    else:
        print(f"Case {case_number}: VIOLATION")