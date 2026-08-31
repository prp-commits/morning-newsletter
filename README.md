# Morning Book Newsletter

A small, dependency-free pipeline that turns a shelf of non-fiction books into a
daily 3-minute email. Every weekday morning it selects a few ideas on that day's
theme, formats them, and sends them — never repeating an idea until the well runs dry.

It currently runs on **16 books and 470+ extracted ideas across five themes**, sending
on an automated daily schedule.

---

## Why it exists

I read faster than I retain. Highlights pile up in apps I never reopen, and a book's
best ideas are effectively gone a month after I finish it. I wanted the opposite of a
reading app: no dashboard to visit, no backlog to feel guilty about. Just a short,
themed email that shows up on its own and resurfaces one good idea at a time.

So the problem is really a content-pipeline problem: **take messy source material,
give it a structure, and deliver the right slice of it on a schedule without repeats.**

## How it works

The flow is deliberately boring and inspectable — five stages, plain files, no database:

| Stage | What happens | Where |
|---|---|---|
| **Ingest** | Each book is extracted into a JSON file: book metadata + a list of self-contained ideas (headline, principle, example, theme tags). | `idea_bank/*.json` |
| **Normalize** | All per-book files are flattened into one pool of ideas, each stamped with its source book and author. | `load_idea_bank()` in `sampler.py` |
| **Route** | Day of week → theme (Mon = Leadership, Tue = Economics, …). Each theme has a *register*: `actionable` themes render a concrete "do this" block; `conceptual` themes stay reflective. | `config.json` + `sampler.py` |
| **Select** | Pick N unsent ideas for today's theme. A `sent_log.json` guarantees no repeats; when a theme's pool is exhausted it gracefully resets rather than failing. Saturdays send a single "favorite" that rotates themes on a 5-week cycle. | `pick_ideas()` / `pick_favorite()` |
| **Deliver** | Format the ideas into a clean responsive HTML email and send over Gmail SMTP. A `--dry-run` flag writes an HTML preview to disk instead of sending. | `sender.py` |

The scheduler (macOS `launchd`) wakes the job every morning; `config.json` decides
whether anything actually goes out that day.

## Design decisions & tradeoffs

A few choices are worth calling out, because they're the interesting part:

- **Flat JSON files, no database.** With a few hundred ideas, a database would be
  overhead I'd have to maintain. Plain files mean the whole system is greppable,
  diff-able, and editable by hand — and adding a book is just dropping in a file.
  The tradeoff: this wouldn't scale to millions of records, and I chose the simple
  thing on purpose.

- **One source of truth for the schedule (learned the hard way).** The schedule
  originally lived in *two* places: `config.json` (what to send) and the scheduler
  (which days to fire). Adding a Sunday theme to config silently did nothing, because
  the scheduler didn't fire on Sundays — a failure with no error. The fix was to make
  the scheduler fire *every* day and let `config.json` be the only knob: on an
  unscheduled day the script simply exits. The bug is now impossible by construction.

- **Register system (actionable vs conceptual).** Leadership and parenting ideas earn
  their keep by being *applied*, so those emails end with a concrete action. Philosophy
  and mental-models ideas are better sat with than acted on. Same pipeline, different
  treatment, driven entirely by config.

- **Fail-fast, with a dry run for confidence.** Missing SMTP credentials or an empty
  theme pool cause a clean exit with a clear message rather than a half-sent email.
  `--dry-run` renders the exact email to `preview.html` without sending, so changes can
  be checked before they hit an inbox.

- **Zero dependencies.** Python 3 standard library only. Nothing to install, nothing
  to keep patched, nothing to break in a year.

## The idea bank (kept local by design)

The heart of the system is the `idea_bank/` directory — one JSON file per book. **That
folder is intentionally *not* in this repository.** The extracted ideas are derived from
copyrighted books and are for my own personal use, so publishing them isn't appropriate.
The code that consumes them is what's interesting and what's shared here.

To make the structure concrete, [`idea_bank.example.json`](idea_bank.example.json) ships
a small illustrative file. Drop a copy into `idea_bank/` and the pipeline will run against
it end to end.

Each file follows this schema:

```jsonc
{
  "schema_version": "0.3",
  "book": {
    "id": "book-slug-author-year",
    "title": "Book Title",
    "subtitle": "Optional Subtitle",
    "authors": ["Author Name"],
    "year": 2024,
    "themes": ["mental_models", "leadership"],
    "source_filename": "original-file.epub",
    "extracted_at": "ISO-8601 timestamp",
    "word_count_estimate": 68000,
    "extraction_note": "provenance / caveats"
  },
  "ideas": [
    {
      "id": "book-slug-author-year__001",   // stable, unique — this is the dedup key
      "headline": "One-line hook",
      "principle": "The idea, in the author's spirit.",
      "author_example": "A concrete illustration from the book.",
      "actionable_insight": "Optional — rendered only on 'actionable' themes.",
      "themes": ["mental_models"],            // an idea may belong to several themes
      "chapter": "4",
      "section": "Optional"
    }
  ]
}
```

The one field the whole system leans on is the idea `id`: it's the dedup key the sent-log
tracks, so it must be stable and unique.

## Repository layout

```
morning-newsletter/
├── sampler.py               # Ingest + normalize + route + select
├── sender.py                # Format + deliver (Gmail SMTP)
├── config.example.json      # Copy to config.json and fill in your details
├── idea_bank.example.json   # Illustrative schema sample
├── README.md
│
│   # kept local, not tracked (see .gitignore):
├── config.json              # real email addresses
├── idea_bank/               # extracted book ideas
└── sent_log.json            # runtime state: what's been sent
```

## Run it yourself

Requires Python 3.10+ (standard library only) and a Gmail account.

```bash
# 1. Configure
cp config.example.json config.json      # then edit the "to" / "from" addresses

# 2. Provide a Gmail App Password (not your real password)
#    Create one at https://myaccount.google.com/apppasswords
export GMAIL_APP_PASSWORD="your16charapppassword"

# 3. Add at least one idea file
mkdir -p idea_bank && cp idea_bank.example.json idea_bank/

# 4. Preview without sending (writes preview.html, updates the sent log)
python3 sender.py --dry-run

# 5. Send for real
python3 sender.py
```

To automate it, schedule `sender.py` to run each morning with `cron` or `launchd`,
passing `GMAIL_APP_PASSWORD` into the job's environment. Keep the scheduler firing
every day and let `config.json` decide which days actually send.

Reset anytime with `rm sent_log.json` (re-sends everything from scratch).

## Status & limitations

Running in production for my own inbox. Deliberately scoped small, so the honest edges:

- **Extraction is upstream of this repo.** Turning a book into a schema-valid JSON file
  is a separate step; this pipeline consumes those files, it doesn't produce them.
- **Input validation is fail-fast, not tolerant.** A malformed JSON file in `idea_bank/`
  will stop the run rather than being skipped — fine for a single-user system I control,
  but the first thing I'd harden for anything multi-source.
- **Single recipient, single sender.** It's a personal tool, not a mailing platform.
