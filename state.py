from typing import TypedDict, Dict, List

class TriageState(TypedDict, total=False):
    patient_id: str
    age: int
    history: List[str]
    symptoms: str
    lab_results: Dict

    history_analysis: str
    symptoms_analysis: str
    lab_analysis: str
    memory_context: str

    risk_score: int
    risk_flags: List[str]

    priority: str
    confidence: float
    reasoning: str
