import os

MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

# Use system ptxas，for B300 machine
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

print(f"Begin model service: {MODEL_NAME}")
print(f"Using system ptxas: {os.environ['TRITON_PTXAS_PATH']}")
os.system(cmd)
