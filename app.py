from graph import app

patient_case = {
    "patient_id": "P1001",
    "age": 72,
    "history": ["diabetes", "hypertension"],
    "symptoms": "Chest pain and shortness of breath",
    "lab_results": {
        "troponin": 0.8,
        "oxygen": 87,
        "bp": "180/120"
    }
}

result = app.invoke(patient_case)

print("""
=== TRIAGE RESULT ===
""")
print('Priority:', result['priority'])
print('Confidence:', result['confidence'])
print("""
Reasoning:
""")
print(result['reasoning'])
