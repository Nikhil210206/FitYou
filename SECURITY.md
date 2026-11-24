# Security Policy

## Supported versions

Only the latest code on the `main` branch (and the live deployment built from it) receives security fixes.

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

Report vulnerabilities privately through GitHub:
[**Report a vulnerability**](https://github.com/Nikhil210206/FitYou/security/advisories/new)

Include as much detail as you can:

- what the issue is and where it lives (file, route or page)
- steps to reproduce, or a proof of concept
- the impact you think it has

You can expect an acknowledgement within 7 days. Once a fix ships, we will credit you in the advisory unless you prefer to stay anonymous.

## Security measures in FitYou

- Passwords are hashed with Werkzeug (never stored in plain text).
- All forms and JSON endpoints are protected against CSRF (Flask-WTF).
- Session cookies are `HttpOnly`, `SameSite=Lax`, and `Secure` in production.
- The app refuses to start in production without a `SECRET_KEY`.
- Login redirects only go to paths on this site (no open redirects).
- Secrets such as `GEMINI_API_KEY` are read from environment variables and never committed.

## For self-hosters

- Generate a strong `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`
- Use a hosted Postgres database with TLS for `DATABASE_URL` in production.
- Keep dependencies up to date (`pip install -U -r requirements.txt`).
