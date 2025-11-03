from typing import Dict, Any

class Metrics:
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.histograms: Dict[str, list[float]] = {}

    def inc(self, name: str, value: int = 1):
        self.counters[name] = self.counters.get(name, 0) + value

    def observe_latency(self, name: str, value: float):
        self.histograms.setdefault(name, []).append(value)

    def snapshot(self) -> Dict[str, Any]:
        return {"counters": self.counters, "histograms": self.histograms}