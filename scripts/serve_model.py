#!/usr/bin/env python3
"""启动 vLLM 模型服务"""
import os

MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

cmd = f"""
python -m vllm.entrypoints.openai.api_server \\
    --model {MODEL_NAME} \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --max-model-len 4096 \\
    --trust-remote-code
"""

print(f"启动模型服务: {MODEL_NAME}")
os.system(cmd)
