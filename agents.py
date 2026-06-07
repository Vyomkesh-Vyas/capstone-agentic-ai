from langchain_ollama import ChatOllama
from memory_store import retrieve_similar_cases, save_case
from langchain_groq import ChatGroq 

GROQ_API_KEY = "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"
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",  # Updated model name
    temperature=0.2,
    max_tokens=1024
)


def intake_agent(state):
    return state


def history_agent(state):
    prompt = f"Analyze medical history risks: {state['history']}"
    response = llm.invoke(prompt)
    return {"history_analysis": response.content}


def symptom_agent(state):
    prompt = f"Analyze emergency symptoms: {state['symptoms']}"
    response = llm.invoke(prompt)
    return {"symptoms_analysis": response.content}


def lab_agent(state):
    prompt = f"Analyze patient lab values: {state['lab_results']}"
    response = llm.invoke(prompt)
    return {"lab_analysis": response.content}


def memory_agent(state):
    memory = retrieve_similar_cases(state['symptoms'])
    return {"memory_context": memory}


def risk_agent(state):
    score = 0
    flags = []

    symptoms = state['symptoms'].lower()
    labs = state['lab_results']

    if 'chest pain' in symptoms:
        score += 40
        flags.append('Possible cardiac issue')

    if labs.get('oxygen', 100) < 90:
        score += 30
        flags.append('Low oxygen')

    if labs.get('troponin', 0) > 0.4:
        score += 40
        flags.append('Elevated troponin')

    return {
        "risk_score": score,
        "risk_flags": flags
    }


def triage_agent(state):
    score = state['risk_score']

    if score >= 80:
        priority = 'P1'
        confidence = 0.97
    elif score >= 60:
        priority = 'P2'
        confidence = 0.91
    elif score >= 30:
        priority = 'P3'
        confidence = 0.82
    else:
        priority = 'P4'
        confidence = 0.70

    return {
        "priority": priority,
        "confidence": confidence
    }


def review_agent(state):
    reasoning = f"""
Priority: {state['priority']}
Confidence: {state['confidence']}
Flags: {state['risk_flags']}

History Analysis:
{state.get('history_analysis')}

Symptoms Analysis:
{state.get('symptoms_analysis')}

Lab Analysis:
{state.get('lab_analysis')}

Memory Context:
{state.get('memory_context')}
"""

    save_case(state['patient_id'], reasoning)

    return {
        "reasoning": reasoning
    }
