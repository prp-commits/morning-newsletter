"""
sender.py — Formats and sends the morning newsletter email.

Uses Gmail SMTP with an App Password (not your real password).
Reads ideas from sampler.py, formats as HTML, sends.
"""

import json
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sampler import sample_for_today


THEME_LABELS = {
    "leadership": "Leadership",
    "economics": "Economics & Personal Finance",
    "mental_models": "Mental Models",
    "philosophy": "Philosophy",
    "parenting": "Parenting",
}


def format_idea_html(idea: dict, index: int, register: str) -> str:
    """Format a single idea as an HTML block."""
    headline = idea["headline"]
    principle = idea["principle"]
    example = idea.get("author_example", "")
    action = idea.get("actionable_insight", "")
    author = idea["_book_author"]
    book = idea["_book_title"]

    example_html = ""
    if example:
        example_html = f"""
        <div style="padding-left:12px;border-left:2px solid #ddd;margin:10px 0;">
            <p style="font-size:13px;font-style:italic;color:#666;line-height:1.6;margin:0;">{example}</p>
        </div>"""

    action_html = ""
    if action and register == "actionable":
        action_html = f"""
        <div style="background:#f7f7f5;border-radius:8px;padding:10px 14px;margin:10px 0;">
            <p style="font-size:11px;font-weight:500;letter-spacing:0.04em;color:#999;margin:0 0 4px;">ACTION</p>
            <p style="font-size:13px;line-height:1.55;margin:0;color:#333;">{action}</p>
        </div>"""

    return f"""
    <div style="margin-bottom:28px;">
        <p style="font-size:11px;font-weight:500;letter-spacing:0.05em;color:#999;margin:0 0 8px;">IDEA {index}</p>
        <p style="font-size:17px;font-weight:500;margin:0 0 10px;line-height:1.4;color:#1a1a1a;">{headline}</p>
        <p style="font-size:14px;line-height:1.65;margin:0 0 10px;color:#333;">{principle}</p>
        {example_html}
        {action_html}
        <p style="font-size:12px;color:#999;margin:8px 0 0;">{author}, <em>{book}</em></p>
    </div>"""


def format_email_html(theme: str, ideas: list[dict], register: str) -> str:
    """Build the complete HTML email body."""
    theme_display = theme
    for key, label in THEME_LABELS.items():
        if key in theme:
            theme_display = label
            break

    day_name = datetime.now().strftime("%A")
    date_str = datetime.now().strftime("%B %d, %Y")

    is_favorite = "favorite" in theme
    if is_favorite:
        subtitle = "The standout idea from this week's rotation"
    else:
        subtitle = f"{len(ideas)} ideas on today's theme"

    ideas_html = ""
    for i, idea in enumerate(ideas, 1):
        ideas_html += format_idea_html(idea, i, register)

    word_count = sum(
        len(idea.get("principle", "").split())
        + len(idea.get("author_example", "").split())
        + len(idea.get("actionable_insight", "").split()) * (1 if register == "actionable" else 0)
        for idea in ideas
    )
    read_time = max(1, round(word_count / 200))

    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:640px;margin:0 auto;padding:20px;color:#333;background:#fff;">

        <div style="border-bottom:1px solid #eee;padding-bottom:12px;margin-bottom:24px;">
            <p style="font-size:12px;color:#999;margin:0 0 4px;">{day_name} · {date_str}</p>
            <p style="font-size:20px;font-weight:500;margin:0 0 4px;color:#1a1a1a;">{theme_display}</p>
            <p style="font-size:13px;color:#999;margin:0;">{subtitle}</p>
        </div>

        {ideas_html}

        <div style="border-top:1px solid #eee;padding-top:12px;margin-top:8px;">
            <p style="font-size:12px;color:#999;margin:0;">~{word_count} words · {read_time} min read</p>
        </div>

    </body>
    </html>"""


def build_subject(theme: str) -> str:
    """Build the email subject line."""
    day_name = datetime.now().strftime("%A")
    theme_display = theme
    for key, label in THEME_LABELS.items():
        if key in theme:
            theme_display = label
            break
    return f"Morning Read · {day_name} · {theme_display}"


def send_email(config: dict, subject: str, html_body: str):
    """Send the email via Gmail SMTP."""
    # App password should be in env var GMAIL_APP_PASSWORD
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        print("ERROR: Set GMAIL_APP_PASSWORD environment variable.")
        print("Generate one at: https://myaccount.google.com/apppasswords")
        sys.exit(1)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config["email"]["from"]
    msg["To"] = config["email"]["to"]

    # Plain text fallback
    plain = "Your morning newsletter is ready. View in an HTML-capable email client."
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"]) as server:
            server.starttls()
            server.login(config["email"]["from"], password)
            server.sendmail(config["email"]["from"], config["email"]["to"], msg.as_string())
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"ERROR sending email: {e}")
        sys.exit(1)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "config.json")) as f:
        config = json.load(f)

    theme, ideas, register = sample_for_today(config)

    if theme is None:
        print(f"No email scheduled for {datetime.now().strftime('%A')}. Exiting.")
        return

    if not ideas:
        print(f"No ideas available for theme '{theme}'. Exiting.")
        return

    subject = build_subject(theme)
    html = format_email_html(theme, ideas, register)

    # Check for --dry-run flag
    if "--dry-run" in sys.argv:
        print(f"DRY RUN — would send: {subject}")
        print(f"Theme: {theme} ({register})")
        print(f"Ideas: {len(ideas)}")
        for i in ideas:
            print(f"  [{i['id']}] {i['headline']}")

        # Save HTML preview
        preview_path = os.path.join(base_dir, "preview.html")
        with open(preview_path, "w") as f:
            f.write(html)
        print(f"\nHTML preview saved to: {preview_path}")
        return

    send_email(config, subject, html)


if __name__ == "__main__":
    main()
