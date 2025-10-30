from typing import List

def simulate_user_turns(task: str) -> List[str]:
    # Deterministic simulation for reproducibility
    # In real voice systems, these are STT transcripts.
    return [
        task,
        "Yes, that's correct.",
        "No other changes needed.",
        "Thanks."
    ]
