# Qwen2.5-Coder HumanEval 评估

## 环境设置

1. 安装依赖 (已完成):
```bash
uv sync
```

2. 启动模型服务:
```bash
uv run python scripts/serve_model.py
```

服务将在 http://localhost:8000 启动

## 测试服务

```bash
curl http://localhost:8000/v1/models
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

需要 Docker 环境来运行测试
