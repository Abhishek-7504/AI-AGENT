import json
from agents.summarizer_agent import SummarizerAgent
from agents.task_extractor_agent import TaskExtractorAgent
import re

def extract_json_block(text):
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match: 
        return match.group(0)
    else:
        raise ValueError("No valid JSON object found in text.")


# Load transcript
with open("sample_transcript.json") as f:
    data = json.load(f)

# Initialize agents
summarizer = SummarizerAgent()
task_extractor = TaskExtractorAgent()

# Run summarizer
summary = summarizer.run(data)
print(summary)

# Run task extractor
tasks = task_extractor.run(data)
print("\nAction Items:\n", tasks)

from agents.email_agent import EmailAgent

# Simulated emails for each person
emails = {
    "Asif": "asifaliahmedrafiq@gmail.com",
    "Kiran": "holambc5@gmail.com",
    "Sanjay": "sanjaydayanandsetty@gmail.com",
    "Abhi": "abhiga304@gmail.com",
    "Pratheek": "pratheekkachinthaya@gmail.com"
}

email_agent = EmailAgent()

try:
    json_text = extract_json_block(tasks)
    parsed_tasks = json.loads(json_text)
except Exception as e:
    print(" Could not extract valid JSON from model output.")
    print("Model returned:\n", tasks)
    raise e


for person, task in parsed_tasks.items():
    # Send emails...
    email_agent.send_email(
        to_email=emails.get(person, "default@example.com"),
        subject="Your Meeting Summary & Action Item",
        summary=summary,
        task=task
    )

