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
        """Return (target_mode, send_command)."""
        target = self._target(temp, occupied)
        send_command = target != self.previous_mode
        self.previous_mode = target
        return target, send_command
def run_stateful_trace(title, percepts):
    """Run a fresh stateful agent over percepts and print a trace table."""
    print("\n" + title)
    print("-" * 74)
    print(f"{'Step':<5}{'Previous':<10}{'Percept':<15}{'Target':<8}{'Outcome'}")
    print("-" * 74)
    agent = StatefulClassroomAgent()
    for step, percept in enumerate(percepts, 1):
        prev = agent.previous_mode
        target, send = agent.act(*percept)
        outcome = "SEND command" if send else "no command"
        print(f"{step:<5}{str(prev):<10}{str(percept):<15}{target:<8}{outcome}")
class HysteresisAgent:
    """COOL turns on above 26.5 C and only turns off below 25.5 C."""
    def __init__(self):
        self.mode = None
    def act(self, temp, occupied):
        if not occupied:
            target = "ECO"
        elif self.mode == "COOL":
            target = "COOL" if temp >= 25.5 else "IDLE"
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
    print("PART A: Reflex agent trace (section 2.5)")
    print("-" * 74)
    reflex = ClassroomAgent()
    percepts = [(29, True), (29, True), (20, True),
                (26, True), (19, True), (29, False)]
    expected = ["COOL", "COOL", "IDLE", "IDLE", "WARM", "ECO"]
    for step, percept in enumerate(percepts, 1):
        mode = reflex.act(*percept)
        ok = "OK" if mode == expected[step - 1] else "MISMATCH"
        print(step, percept, "target mode", mode, f"[{ok}]")
    print("Note: COOL is returned twice, the reflex agent has no memory.")
    print("\nPART B: Stateful agent (Task 3)")
    run_stateful_trace(
        "Test 1: Repeated percepts (same input three times)",
        [(29, True), (29, True), (29, True)])
    run_stateful_trace(
        "Test 2: Exact boundaries (20 C and 26 C, occupied)",
        [(20, True), (26, True), (19.9, True), (26.1, True)])
    run_stateful_trace(
        "Test 3: Mode transition (IDLE -> COOL -> IDLE -> WARM)",
        [(24, True), (29, True), (24, True), (18, True)])
    run_stateful_trace(
        "Test 4: Empty-room case (occupancy priority over temperature)",
        [(29, True), (29, False), (29, False), (15, False), (29, True)])
    noisy = [(26.2, True), (25.9, True), (26.3, True),
             (25.8, True), (26.4, True), (25.7, True)]
    print("\nPART C: Noisy sequence around 26 C (comparison)")
    run_stateful_trace(
        "Stateful agent WITHOUT hysteresis (same thresholds)", noisy)
    print("\nStateful agent WITH hysteresis (ON > 26.5, OFF < 25.5)")
    print("-" * 74)
    print(f"{'Step':<5}{'Previous':<10}{'Percept':<15}{'Target':<8}{'Outcome'}")
    print("-" * 74)
    h = HysteresisAgent()
    for step, percept in enumerate(noisy, 1):
        prev = h.mode
        target, send = h.act(*percept)
        outcome = "SEND command" if send else "no command"
        print(f"{step:<5}{str(prev):<10}{str(percept):<15}{target:<8}{outcome}")
    plain, hyst = StatefulClassroomAgent(), HysteresisAgent()
    n_plain = sum(plain.act(*p)[1] for p in noisy)
    n_hyst = sum(hyst.act(*p)[1] for p in noisy)
    print(f"\nCommands sent -> without hysteresis: {n_plain}, "
          f"with hysteresis: {n_hyst}")

