from langgraph.graph import StateGraph, END
from state import TriageState

from agents import (
    intake_agent,
    history_agent,
    symptom_agent,
    lab_agent,
    memory_agent,
    risk_agent,
    triage_agent,
    review_agent
)

workflow = StateGraph(TriageState)

workflow.add_node('intake', intake_agent)
workflow.add_node('history', history_agent)
workflow.add_node('symptom', symptom_agent)
workflow.add_node('lab', lab_agent)
workflow.add_node('memory', memory_agent)
workflow.add_node('risk', risk_agent)
workflow.add_node('triage', triage_agent)
workflow.add_node('review', review_agent)

workflow.set_entry_point('intake')

workflow.add_edge('intake', 'history')
workflow.add_edge('intake', 'symptom')
workflow.add_edge('intake', 'lab')
workflow.add_edge('intake', 'memory')

workflow.add_edge('history', 'risk')
workflow.add_edge('symptom', 'risk')
workflow.add_edge('lab', 'risk')
workflow.add_edge('memory', 'risk')

workflow.add_edge('risk', 'triage')
workflow.add_edge('triage', 'review')
workflow.add_edge('review', END)

app = workflow.compile()
