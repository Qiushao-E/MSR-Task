# Qwen2.5-Coder-0.5B-Instruct HumanEval 评估

## 环境设置

1. 安装依赖:
```bash
uv sync
```

2. 启动模型服务:

需要docker环境启动服务，使用vllm/vllm-openai:latest镜像
```bash
uv run python scripts/serve_model.py
```
或者在本地启动服务
```bash
uv run python scripts/serve_model_local.py
```

服务将在 http://localhost:3344 启动

## 测试服务

```bash
curl http://localhost:3344/v1/models
```

## 运行推理

```bash
uv run python scripts/inference.py
```

结果保存在 `outputs/humaneval_results.jsonl`

## 运行评估

```bash
uv run python scripts/evaluate.py
```
