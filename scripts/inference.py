#!/usr/bin/env python3
"""HumanEval 推理脚本"""
import json
import os
from openai import OpenAI

# 配置
API_BASE = "http://localhost:8000/v1"
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
INPUT_FILE = "datasets/humaneval/HumanEval.jsonl"
OUTPUT_FILE = "outputs/humaneval_results.jsonl"

def load_humaneval():
    """加载 HumanEval 数据集"""
    problems = []
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems

def generate_code(client, prompt):
    """调用模型生成代码"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a code completion assistant. Complete the given Python function."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.0
    )
    return response.choices[0].message.content

def main():
    """主函数"""
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
