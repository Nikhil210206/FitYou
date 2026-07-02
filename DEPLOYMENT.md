# 🚀 Deployment Guide

This project supports automatic deployment when pull requests are merged to the main branch.

## Supported Platforms

### 1. Render (Recommended)
- **Auto-deploy**: ✅ Built-in GitHub integration
- **Setup**: Connect GitHub repo at [render.com](https://render.com)
- **Config**: Uses `render.yaml` (already configured)
- **Free tier**: 750 CPU hours/month

### 2. Railway
- **Auto-deploy**: ✅ GitHub integration
- **Setup**: Connect repo at [railway.app](https://railway.app)
- **Free tier**: $5 credit/month
- **GitHub Secret**: Add `RAILWAY_TOKEN` for Actions deployment

### 3. Fly.io
- **Auto-deploy**: ✅ Via GitHub Actions
- **Setup**: Install Fly CLI and create app
- **Free tier**: 3 VMs, 2,160 hours/month
- **GitHub Secret**: Add `FLY_API_TOKEN`

### 4. Vercel

- **Setup**: Import the repo at [vercel.com](https://vercel.com); the `vercel.json` routes all traffic to the Flask app (`app.py`).
- **Important**: Vercel's filesystem is read-only/ephemeral, so SQLite cannot be used for auth. You **must** provision a hosted Postgres database (e.g. [Neon](https://neon.tech) or Vercel Postgres) and set `DATABASE_URL`.
- Add the environment variables below in the Vercel dashboard.

## Environment Variables Required

| Variable | Required | Notes |
| --- | --- | --- |
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key ([get one](https://aistudio.google.com/app/apikey)). |
| `SECRET_KEY` | Yes | Long random string for Flask sessions. Generate: `python -c "import secrets; print(secrets.token_hex(32))"`. |
| `DATABASE_URL` | Yes on Vercel | Postgres connection string. Locally defaults to a SQLite file if unset. |
| `GEMINI_MODEL` | No | Overrides the model (default `gemini-2.5-flash`). Retired models are ignored automatically. |
| `PYTHONPATH` | No | Set to `.` (already configured in `vercel.json`). |

> Local development: copy `env_template.txt` to `.env` and fill in the values. Tables are created automatically on first run.

## GitHub Actions Workflow

The `.github/workflows/deploy.yml` file handles automatic deployment:
- Triggers on push to main branch
- Triggers when PRs are merged
- Supports multiple deployment targets
- Includes deployment status notifications

## Quick Start

1. **Choose a platform** (Render recommended)
2. **Connect your GitHub repo** to the platform
3. **Add environment variables** in platform dashboard
4. **Add GitHub Secrets** (if using Railway/Fly.io)
5. **Merge a PR** → Automatic deployment! 🎉

## Troubleshooting

- Check GitHub Actions tab for deployment logs
- Verify environment variables are set correctly
- Ensure `requirements.txt` includes all dependencies
- Check platform-specific logs for detailed error messages