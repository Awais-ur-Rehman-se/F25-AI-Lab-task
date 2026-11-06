class ClassroomAgent:
    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"
class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None
    def _target(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"
    def act(self, temp, occupied):
        target = self._target(temp, occupied)
        send_command = target != self.previous_mode
        self.previous_mode = target
        return target, send_command
def run_stateful_trace(title, percepts):
    print("\n" + title)
    print("-" * 65)
    print("Step   Previous   Percept       Target   Outcome")
    agent = StatefulClassroomAgent()
    for step, percept in enumerate(percepts, 1):
        previous = agent.previous_mode
        target, send = agent.act(*percept)
        if send:
            outcome = "SEND command"
        else:
            outcome = "No command"
        print(step, previous, percept, target, outcome)
class HysteresisAgent:
    def __init__(self):
        self.mode = None
    def act(self, temp, occupied):
        if not occupied:
            target = "ECO"
        elif self.mode == "COOL":
            if temp >= 25.5:
                target = "COOL"
            else:
                target = "IDLE"
        elif temp > 26.5:
            target = "COOL"
        elif temp < 20:
            target = "WARM"
        else:
            target = "IDLE"
        send = target != self.mode
        self.mode = target
        return target, send
if __name__ == "__main__":
    print("PART A: Reflex Agent")
    print("-" * 40)
    reflex = ClassroomAgent()
    percepts = [
        (29, True),
        (29, True),
        (20, True),
        (26, True),
        (19, True),
        (29, False)
    ]
    expected = ["COOL", "COOL", "IDLE", "IDLE", "WARM", "ECO"]
    for step, percept in enumerate(percepts, 1):
        mode = reflex.act(*percept)
        if mode == expected[step - 1]:
            result = "OK"
        else:
            result = "MISMATCH"
        print(step, percept, "Target Mode:", mode, result)
    print("Reflex agent has no memory.")
    print("\nPART B: Stateful Agent")
    run_stateful_trace(
        "Test 1: Repeated inputs",
        [(29, True), (29, True), (29, True)]
    )
    run_stateful_trace(
        "Test 2: Exact boundaries",
        [(20, True), (26, True), (19.9, True), (26.1, True)]
    )
    run_stateful_trace(
        "Test 3: Mode changes",
        [(24, True), (29, True), (24, True), (18, True)]
    )
    run_stateful_trace(
        "Test 4: Empty room",
        [(29, True), (29, False), (29, False),
         (15, False), (29, True)]
    )
    noisy = [
        (26.2, True),
        (25.9, True),
        (26.3, True),
        (25.8, True),
        (26.4, True),
        (25.7, True)
    ]
    print("\nPART C: Hysteresis Comparison")
    run_stateful_trace(
        "Without Hysteresis",
        noisy
    )
    print("\nWith Hysteresis")
    h = HysteresisAgent()
    for step, percept in enumerate(noisy, 1):
        previous = h.mode
        target, send = h.act(*percept)
        if send:
            outcome = "SEND command"
        else:
            outcome = "No command"
        print(step, previous, percept, target, outcome)
    plain = StatefulClassroomAgent()
    hyst = HysteresisAgent()
    normal_count = sum(plain.act(*p)[1] for p in noisy)
    hyst_count = sum(hyst.act(*p)[1] for p in noisy)
    print("\nCommands sent:")
    print("Without hysteresis:", normal_count)
    print("With hysteresis:", hyst_count)
