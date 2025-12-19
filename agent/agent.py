import json
from huggingface_hub import InferenceClient

from agent.tools import (
    search_patient,
    check_insurance_eligibility,
    find_available_slots,
    book_appointment
)

# -------- LLM (DIRECT, NO LANGCHAIN) --------

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=None  # uses HUGGINGFACEHUB_API_TOKEN env var
)

# -------- Tool registry --------

TOOL_MAP = {
    "search_patient": search_patient,
    "check_insurance_eligibility": check_insurance_eligibility,
    "find_available_slots": find_available_slots,
    "book_appointment": book_appointment
}

# -------- Agent --------

def run_agent(user_input: str):
    prompt = f"""
You are a clinical workflow automation agent.

Rules:
- NO medical advice
- NO explanations
- Choose ONE action
- If unsafe or unclear, return:
  {{ "action": "REFUSE", "reason": "<short reason>" }}

Available actions:
1. search_patient(name)
2. check_insurance_eligibility(patient_id)
3. find_available_slots(specialty)
4. book_appointment(patient_id, specialty, date)

User request:
{user_input}

Respond ONLY with valid JSON:
{{
  "action": "<action_name>",
  "arguments": {{ ... }}
}}
"""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a clinical workflow automation agent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=300
    )

    content = response.choices[0].message.content

    try:
        decision = json.loads(content)
    except Exception:
        return {
            "status": "REFUSED",
            "reason": "Model returned invalid JSON"
        }

    if decision.get("action") == "REFUSE":
        return decision

    action = decision.get("action")
    arguments = decision.get("arguments", {})

    if action not in TOOL_MAP:
        return {
            "status": "REFUSED",
            "reason": "Invalid action"
        }

    # -------- orchestration fix (IMPORTANT) --------
    if action == "book_appointment":
        # Step 1: resolve patient_id from name
        if "patient_id" not in arguments and "name" in arguments:
            patient = search_patient({"name": arguments["name"]})
            arguments["patient_id"] = patient["patient_id"]

        # Step 2: resolve vague date like "next week"
        if arguments.get("date") in ["next week", None]:
            slots = find_available_slots({"specialty": arguments["specialty"]})
            arguments["date"] = slots[0]["date"]

    return TOOL_MAP[action](arguments)
