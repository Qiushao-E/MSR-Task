#!/usr/bin/env python3
"""启动 vLLM 模型服务 (Docker)"""
import os
import subprocess

MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
CACHE_DIR = os.path.expanduser("~/.cache/huggingface")

# 确保缓存目录存在
os.makedirs(CACHE_DIR, exist_ok=True)

cmd = [
    "docker", "run", "-d",
    "--name", "vllm-server",
    "-p", "1024:8000",
    "-v", f"{CACHE_DIR}:/root/.cache/huggingface",
    "--ipc=host",
    "vllm/vllm-openai:latest",
    "--model", MODEL_NAME,
    "--host", "0.0.0.0",
    "--port", "8000",
    "--max-model-len", "4096",
    "--trust-remote-code",
    "--device", "cpu",
    "--dtype", "float32"
]

print(f"启动 Docker 容器运行模型服务 (CPU): {MODEL_NAME}")
print(f"缓存目录: {CACHE_DIR}")
print("服务地址: http://localhost:1024")

# 先停止并删除已存在的容器
subprocess.run(["docker", "stop", "vllm-server"], capture_output=True)
subprocess.run(["docker", "rm", "vllm-server"], capture_output=True)

# 启动新容器
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"容器已启动: {result.stdout.strip()}")
    print("\n查看日志: docker logs -f vllm-server")
    print("停止服务: docker stop vllm-server")
else:
    print(f"启动失败: {result.stderr}")
