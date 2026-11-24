# Contributing to FitYou

Thanks for your interest in improving FitYou! This guide covers how to set up the project, make a change, and get it merged.

## Ways to contribute

- **Fix a bug** or pick up an [open issue](https://github.com/Nikhil210206/FitYou/issues)
- **Grow the datasets:** add exercises to `exercises.csv` or dishes to `diet_data.csv`
- **Improve the UI** in `templates/` and `static/css/main.css`
- **Write tests** or improve the docs

If you plan a large change, open an issue first so we can agree on the approach.

## Local setup

```bash
git clone https://github.com/<your-username>/FitYou.git
cd FitYou
git remote add upstream https://github.com/Nikhil210206/FitYou.git
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp env_template.txt .env   # then set GEMINI_API_KEY and SECRET_KEY
flask --app app run --debug
```

The app runs at http://localhost:5000 and creates a local SQLite database on first run.

## Workflow

1. Sync your fork with the latest `main`:
   ```bash
   git checkout main
   git pull upstream main
   ```
2. Create a branch with a descriptive name, such as `feat/macro-chart` or `fix/login-redirect`:
   ```bash
   git checkout -b feat/your-feature
   ```
3. Make your change and check it in the browser (workout generator, diet planner, sports routines, and AI coach if you touched them).
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/) style:
   ```bash
   git commit -m "feat: add macro breakdown to diet plan"
   ```
5. Push and open a pull request against `main`:
   ```bash
   git push -u origin feat/your-feature
   ```
6. Fill in the pull request template, link the issue (for example `Fixes #12`), and add screenshots for UI changes.

## Guidelines

- Keep pull requests focused on one change.
- Follow the existing style: PEP 8 for Python, the CSS variables in `static/css/main.css` for styling.
- Never commit secrets. `.env` is gitignored; use `env_template.txt` to document new variables.
- When adding dataset rows, keep the existing columns and value formats (for example `goal` is `weight_loss`, `weight_gain` or `maintenance`).

## Resolving merge conflicts

```bash
git checkout main && git pull upstream main
git checkout feat/your-feature && git merge main
# fix the files marked with <<<<<<< ======= >>>>>>>, then:
git add .
git commit
git push
```

## Reporting security issues

Please do not open public issues for vulnerabilities. Follow [SECURITY.md](SECURITY.md) instead.
