from agent.agent import run_agent

query = "Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility"
#query = "Hello World"
result = run_agent(query)
print(result)
