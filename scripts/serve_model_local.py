#!/usr/bin/env python3
"""启动 vLLM 模型服务"""
import os

MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

# 设置环境变量使用系统 ptxas
os.environ['TRITON_PTXAS_PATH'] = '/usr/local/cuda/bin/ptxas'

cmd = f"""
python -m vllm.entrypoints.openai.api_server \\
    --model {MODEL_NAME} \\
    --host 0.0.0.0 \\
    --port 1024 \\
    --max-model-len 4096 \\
    --trust-remote-code \\
    --gpu-memory-utilization 0.3 \\
"""
    # --generation-config vllm \\
print(f"启动模型服务: {MODEL_NAME}")
print(f"使用系统 ptxas: {os.environ['TRITON_PTXAS_PATH']}")
os.system(cmd)
