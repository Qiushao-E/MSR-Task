import json
import os
from openai import OpenAI

API_BASE = "http://localhost:3344/v1"
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
# MODEL_NAME = "/hub/models--Qwen--Qwen2.5-Coder-0.5B-Instruct/snapshots/ea3f2471cf1b1f0db85067f1ef93848e38e88c25"
INPUT_FILE = "datasets/humaneval/HumanEval.jsonl"
OUTPUT_FILE = "outputs/humaneval_results.jsonl"

def load_humaneval():
    problems = []
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems

def extract_code(text):
    if "```python" in text:
        text = text.split("```python")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()

def generate_code(client, prompt):
    instruction = f"""Complete the following Python function. Only provide the complete function implementation, no explanations.

{prompt}"""
    system_prompt = "You are an expert Python coding assistant. Return only runnable Python code. Do not include markdown, explanations, tests, or multiple alternatives."

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction}
        ],
        max_tokens=1024,
        temperature=0.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    completion = response.choices[0].message.content
    return extract_code(completion)

def main():
    client = OpenAI(api_key="EMPTY", base_url=API_BASE)
    problems = load_humaneval()

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_FILE, 'w') as f:
        for i, problem in enumerate(problems):
            print(f"Processing {i+1}/{len(problems)}: {problem['task_id']}")

            completion = generate_code(client, problem['prompt'])

            result = {
                "task_id": problem['task_id'],
                "completion": completion
            }
            f.write(json.dumps(result) + '\n')
            f.flush()

    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
