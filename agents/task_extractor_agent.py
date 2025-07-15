import ollama
from typing import Dict

class TaskExtractorAgent:
    def __init__(self, model='llama3'):
        self.model = model

    def run(self, input_data: Dict):
        transcript = "\n".join([f"{t['speaker']}: {t['text']}" for t in input_data['transcript']])
        prompt = f"""
Extract the action items for each participant based on this transcript.
Return the result as a JSON object like:

{{
  "Alice": "task",
  "Bob": "task"
}}

Transcript:
{transcript}
"""
        response = ollama.chat(model=self.model, messages=[
            {"role": "user", "content": prompt}
        ])
        return response['message']['content']
