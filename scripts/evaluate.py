#!/usr/bin/env python3
"""HumanEval 评估脚本"""
import json
import subprocess
import tempfile
import os
from pathlib import Path

INPUT_FILE = "outputs/humaneval_results.jsonl"
DATASET_FILE = "datasets/humaneval/HumanEval.jsonl"

def load_results():
    """加载推理结果"""
    results = {}
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            item = json.loads(line)
            results[item['task_id']] = item['completion']
    return results

def load_tests():
    """加载测试用例"""
    tests = {}
    with open(DATASET_FILE, 'r') as f:
        for line in f:
            item = json.loads(line)
            tests[item['task_id']] = {
                'prompt': item['prompt'],
                'test': item['test'],
                'entry_point': item['entry_point']
            }
    return tests

def run_test(code, test_code, entry_point):
    """在 Docker 容器中运行测试"""
    test_program = f"{code}\n{test_code}\ncheck({entry_point})"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_program)
        temp_file = f.name

    try:
        result = subprocess.run(
            ['docker', 'run', '--rm', '-v', f'{temp_file}:/test.py',
             'python:3.10-slim', 'python', '/test.py'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False
    finally:
        os.unlink(temp_file)

def main():
    """主函数"""
    results = load_results()
    tests = load_tests()

    passed = 0
    total = 0

    for task_id in results:
        if task_id not in tests:
            continue

        total += 1
        completion = results[task_id]
        test_info = tests[task_id]

        print(f"Testing {task_id}...", end=" ")

        success = run_test(completion, test_info['test'], test_info['entry_point'])

        if success:
            passed += 1
            print("✓")
        else:
            print("✗")

    pass_rate = passed / total if total > 0 else 0
    print(f"\nResults: {passed}/{total} passed ({pass_rate*100:.2f}%)")

if __name__ == "__main__":
    main()
