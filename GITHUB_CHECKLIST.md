# GitHub Checklist

Before publishing this project to GitHub, check the following items.

## Security

- Do not commit API keys.
- Do not include `.env` files with real secrets.
- Keep only `.env.example`.
- If a key has appeared in chat or logs, rotate it in the DashScope console.
- Public users can run `Model mode = heuristic` without any API key.
- `Model mode = qwen_api` requires each user to provide their own
  `DASHSCOPE_API_KEY`.

## Files To Keep

- `README.md`
- `INTERVIEW_NOTES.md`
- `RESUME_VARIANTS.md`
- `src/`
- `app.py`
- `cli.py`
- `scripts/create_demo_data.py`
- `configs/model_adapters.yaml`
- `requirements.txt`
- `Dockerfile`
- `demo_data/pre.png`
- `demo_data/post.png`
- selected demo outputs, if you want screenshots in the repository

## Files To Avoid Committing

- Real API keys
- `.env`
- temporary logs
- large model weights
- large datasets
- unnecessary cache folders

## Recommended Screenshots

1. Gradio page with pre/post images.
2. Change overlay and binary mask.
3. Evidence metrics JSON.
4. Qwen-VL Chinese structured report.

## Recommended GitHub Description

```text
Remote-sensing multimodal interpretation Agent with change-mask extraction,
Qwen-VL API reasoning, RAG-style domain context, and Gradio visualization.
```

## Recommended Repository Name

```text
GeoVLM-ChangeAgent
```
