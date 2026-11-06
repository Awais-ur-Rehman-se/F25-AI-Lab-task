# Task 2: Scholarship Screening System
def scholarship_check(score, documents, attendance, income):
    if score < 70:
        return "Hold", "Score is below 70"
    elif documents == False:
        return "Hold", "Documents are incomplete"
    elif attendance < 80:
        return "Hold", "Attendance is below 80%"
    elif income > 50000:
        return "Hold", "Family income is above 50000"
    else:
        return "Review", "All four conditions passed"
def probability_check(probability):
    if probability >= 0.70:
        return "Review"
    else:
        return "Hold"
test_cases = [
    {
        "name": "Full Pass",
        "score": 85,
        "documents": True,
        "attendance": 90,
        "income": 40000,
        "probability": 0.82,
        "expected": "Review"
    },
    {
        "name": "Attendance Failure",
        "score": 82,
        "documents": True,
        "attendance": 79,
        "income": 40000,
        "probability": 0.81,
        "expected": "Hold"
    },
    {
        "name": "Income Failure",
        "score": 88,
        "documents": True,
        "attendance": 90,
        "income": 51000,
        "probability": 0.88,
        "expected": "Hold"
    },
    {
        "name": "Boundary Case",
        "score": 70,
        "documents": True,
        "attendance": 80,
        "income": 50000,
        "probability": 0.70,
        "expected": "Review"
    }
]
print("SCHOLARSHIP SCREENING SYSTEM")
print("--------------------------------")
all_passed = True
for case in test_cases:
    actual, reason = scholarship_check(
        case["score"],
        case["documents"],
        case["attendance"],
        case["income"]
    )
    probability_result = probability_check(
        case["probability"]
    )
    print("\nTest Case:", case["name"])
    print("Input:",
          "Score =", case["score"],
          "Documents =", case["documents"],
          "Attendance =", case["attendance"],
          "Income =", case["income"],
          "Probability =", case["probability"])
    print("Expected Result:", case["expected"])
    print("Actual Result:", actual)
    print("Reason:", reason)
    print("Probability Result:", probability_result)
    print("Disagreement:", actual != probability_result)
    if actual == case["expected"]:
        print("Test Status: PASS")
    else:
        print("Test Status: FAIL")
        all_passed = False
print("\n--------------------------------")
if all_passed:
    print("All four core tests passed.")
else:
    print("Some tests failed.")
print("\nRULES VS PROBABILITY COMPARISON")
print("--------------------------------")
examples = [
    ("complete_low", 68, True, 90, 40000, 0.74),
    ("incomplete_high", 91, False, 90, 40000, 0.88)
]
for name, score, documents, attendance, income, probability in examples:

    rule_result, reason = scholarship_check(
        score, documents, attendance, income
    )
    prob_result = probability_check(probability)
    print("\nExample:", name)
    print("Rule Result:", rule_result)
    print("Probability Result:", prob_result)
    print("Reason:", reason)
    print("Disagreement:", rule_result != prob_result)
print("\nBOUNDARY CHECKS")
print("--------------------------------")
print("Score 70:",
      scholarship_check(70, True, 80, 50000)[0])
print("Score 69:",
      scholarship_check(69, True, 80, 50000)[0])
print("Probability 0.70:",
      probability_check(0.70))
print("Probability 0.69:",
      probability_check(0.69))
