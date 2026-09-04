import random


# -----------------------------
# DECLARE constraints
# -----------------------------

def response(trace, A, B):
    """
    Response(A, B):

    Om A inträffar måste B inträffa senare i tracen.
    """

    for i, activity in enumerate(trace):

        if activity == A:

            # Finns B efter A?
            if B not in trace[i + 1:]:
                return False

    return True


def precedence(trace, A, B):
    """
    Precedence(A, B):

    Om B inträffar måste A ha inträffat tidigare.
    """

    for i, activity in enumerate(trace):

        if activity == B:

            # Finns A före B?
            if A not in trace[:i]:
                return False

    return True


def not_coexistence(trace, A, B):
    """
    A och B får inte båda förekomma.
    """

    return not (A in trace and B in trace)


# -----------------------------
# Random agent
# -----------------------------

activities = [
    "Request",
    "Review",
    "Approve",
    "Reject"
]


def random_agent(num_steps=5):

    trace = []

    for _ in range(num_steps):

        action = random.choice(activities)

        trace.append(action)

    return trace


# -----------------------------
# DECLARE model
# -----------------------------

def check_trace(trace):

    results = {}

    results["Response(Request, Review)"] = response(
        trace,
        "Request",
        "Review"
    )

    results["Precedence(Review, Approve)"] = precedence(
        trace,
        "Review",
        "Approve"
    )

    results["NotCoExistence(Approve, Reject)"] = not_coexistence(
        trace,
        "Approve",
        "Reject"
    )

    return results


# -----------------------------
# Run simulation
# -----------------------------
print("=================== SIMULATION 1 ===================")
trace = random_agent()

print("TRACE:")
print(trace)

print("\nCONSTRAINTS:")

results = check_trace(trace)

for constraint, satisfied in results.items():

    print(
        constraint,
        "->",
        "SATISFIED" if satisfied else "VIOLATED"
    )

# -----------------------------
# Run simulation 2
# -----------------------------

print("=================== SIMULATION 2 ===================")

trace = activities
trace.pop()

print(f"Trace: {trace}")

print("\nCONSTRAINTS:")



results = check_trace(trace)

for constraint, satisfied in results.items():

    print(
        constraint,
        "->",
        "SATISFIED" if satisfied else "VIOLATED"
    )

