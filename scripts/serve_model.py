import os
import subprocess

MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
CACHE_DIR = os.path.expanduser("~/.cache/huggingface")

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
]

print(f"Starting Docker container for model service: {MODEL_NAME}")
print(f"Cache directory: {CACHE_DIR}")
print("Service URL: http://localhost:1024")

subprocess.run(["docker", "stop", "vllm-server"], capture_output=True)
subprocess.run(["docker", "rm", "vllm-server"], capture_output=True)

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"Container started: {result.stdout.strip()}")
    print("\nView logs: docker logs -f vllm-server")
    print("Stop service: docker stop vllm-server")
else:
    print(f"Failed to start: {result.stderr}")
