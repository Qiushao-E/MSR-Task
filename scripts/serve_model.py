import os
import subprocess


# Change to model hash 
MODEL_NAME = "/hub/models--Qwen--Qwen2.5-Coder-0.5B-Instruct/snapshots/ea3f2471cf1b1f0db85067f1ef93848e38e88c25"
HUB_DIR = os.path.expanduser("~/.cache/huggingface/hub")

cmd = [
    "docker", "run", "-d",
    "--name", "vllm-server",
    "--gpus", '"device=1"',
    "-e", "HF_HUB_OFFLINE=1",
    "--network=host", 
    "-v", f"{HUB_DIR}:/hub", 
    "--ipc=host",
    "vllm/vllm-openai:latest",
    "--model", MODEL_NAME,
    "--host", "0.0.0.0",
    "--port", "3344",
    "--max-model-len", "4096",
    "--trust-remote-code",
]

print(f"Starting Docker container for model service: {MODEL_NAME}")
print(f"Cache directory: {HUB_DIR}")
print("Service URL: http://localhost:3344")

subprocess.run(["docker", "stop", "vllm-server"], capture_output=True)
subprocess.run(["docker", "rm", "vllm-server"], capture_output=True)

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"Container started: {result.stdout.strip()}")
    print("\nView logs: docker logs -f vllm-server")
    print("Stop service: docker stop vllm-server")
else:
    print(f"Failed to start: {result.stderr}")
