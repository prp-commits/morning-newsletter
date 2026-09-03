---
name: book-idea-extractor
description: Extract durable ideas from a non-fiction book into a structured JSON file that feeds a morning book newsletter. Use this skill whenever the user uploads a non-fiction book (epub or pdf) and asks to "extract ideas," "add to the idea bank," "process this for the newsletter," or similar. Also use it when a user uploads one or more books and asks to populate, update, or refresh the `idea-bank` / `idea_bank` JSON collection. Triggers even when the user doesn't explicitly reference the newsletter — if the conversation involves extracting newsletter-worthy ideas from a book into JSON, use this skill.
---

# Book Idea Extractor

Extract durable ideas from a non-fiction book into a single JSON file that slots into the user's morning newsletter idea bank. One chat = one book. Output is a JSON file named `<book-id>.json` that gets dropped into the `idea_bank/` directory.

## When to use

- User uploads a non-fiction book (epub or pdf) for the morning newsletter
- User says "add this to the idea bank" / "extract ideas from this book" / "process this for the newsletter"
- User has an existing idea bank and wants a new book added in the same format

## When NOT to use

- Fiction, memoir without transferable lessons, pure reference manuals (textbooks, API docs), or heavily technical quant books where the value is in equations, not ideas. If the book doesn't have transferable principles, tell the user and stop — don't force-fit.
- Books that don't map to the user's theme set. The current themes are: `trading`, `leadership`, `economics`, `mental_models`, `philosophy`, `parenting`. If the book doesn't fit at least one, flag it and ask the user whether to add a new theme or skip the book.

## Core rule: one book per chat

Do not batch multiple books in a single chat. Quality degrades past one because:
- Context window fills with book text and prior extractions, leaving less room for careful thinking per idea
- Consistency drifts across books when done in sequence
- The user loses the ability to review each book individually

If the user uploads more than one, pick one and flag the rest: "I'll do `<title>` in this chat. Open a new chat and re-upload each of the others — same instructions will trigger this skill again."

## The workflow

### Step 1: Read the book

Copy the book from `/mnt/user-data/uploads/` to `/home/claude/` for working. Then extract its text:

- **epub**: unzip and read the HTML files in order. `unzip -o book.epub -d book_unzipped && find book_unzipped -name '*.xhtml' -o -name '*.html' | sort`
- **pdf**: use `pdftotext` for text-heavy books, or follow the pdf-reading skill (`/mnt/skills/public/pdf-reading/SKILL.md`) for image-heavy / scanned ones

Read enough to build a complete mental map of the book — table of contents, every major chapter's thesis, and the author's representative examples. You do not need to read every word, but you do need to have seen every chapter. Skipping chapters is how you miss the best ideas.

### Step 2: Identify themes

Assign 1–3 themes from the fixed theme set:
- **trading** — actionable market behavior, execution, psychology under pressure in a trading context
- **leadership** — how to lead people, make decisions, build teams, set tone
- **economics** — money, incentives, monetary systems, personal finance, macro
- **mental_models** — thinking tools, cognition, reasoning, decision-making frameworks
- **philosophy** — character, meaning, ethics, virtue, how to live
- **parenting** — raising kids, family, the parent-child relationship, presence, discipline, character formation in children

A book can be multi-themed. *Mind Over Markets* is `trading` + `mental_models`. *On Character* is `leadership` + `mental_models`. *The Daily Dad* is `parenting` + `philosophy` + `mental_models`. Err on the side of fewer themes — a book tagged with five or six themes is a book you haven't read closely.

**`parenting` is an actionable, Sunday-only theme.** In the newsletter schedule it maps to the single Sunday email and is *not* part of the Saturday "favorite" rotation. Like `trading` and `leadership`, it is an actionable register — every parenting-tagged idea must carry an `actionable_insight` (see Step 4). It's a domain theme (like `trading`) that anchors a book and typically pairs with `leadership`, `mental_models`, or `philosophy`.

If the book fits none of these cleanly: **stop and ask the user** whether to add a new theme or skip. Do not force-fit.

### Step 3: Extract ideas

Target **20–40 ideas per book**, depending on density. Mind Over Markets produced 30. On Character produced ~35. A shorter book like The Gap and The Gain might yield 15. Don't pad — if the book genuinely only has 15 strong ideas, extract 15. Don't skimp either.

**What counts as an "idea":**
- A transferable principle the reader can apply, not a summary of a chapter
- Something the author argues, not something the author mentions
- An insight the reader could plausibly remember six months later
- Not a quote — an idea (which may be illustrated with a quote or example)

**What does NOT count:**
- "The author talks about X" — that's a topic, not an idea
- "People should be nice" — too generic to be an idea from this book specifically
- Something you could write without having read this book

### Step 4: Write each idea to the schema

Every idea is an entry with these fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `id` | yes | `<book-id-prefix>-NNN`, e.g. `mom-001` for Mind Over Markets |
| `headline` | yes | One sentence, declarative, no jargon. The email subject line equivalent. |
| `principle` | yes | 2–4 sentences. The idea itself, in plain language. Should stand alone without the example. |
| `author_example` | yes | 2–4 sentences. A concrete case, story, or analogy from the book that illustrates the principle. Use the author's example — don't invent new ones. |
| `actionable_insight` | only for ideas tagged `trading`, `leadership`, or `parenting` | 2–3 sentences. A concrete thing the reader can do, look for, or avoid this week. Not a restatement of the principle. |
| `themes` | yes | Array. Subset of the book's themes — an idea can be narrower than the book. |
| `chapter` | yes | Chapter title or number for citation |
| `section` | optional | If the chapter is long and the idea sits in a specific subsection |

See `references/schema.md` for the full JSON template and `references/examples.md` for worked examples of good vs. bad entries.

### Step 5: Assemble the book-level JSON

Wrap the ideas in a book-level object:

```json
{
  "schema_version": "0.3",
  "book": {
    "id": "slug-author-year",
    "title": "Full title",
    "subtitle": "If present",
    "authors": ["Author Name"],
    "year": 2023,
    "edition": "If notable",
    "themes": ["theme1", "theme2"],
    "source_filename": "exact filename from uploads",
    "extracted_at": "YYYY-MM-DD",
    "word_count_estimate": 75000,
    "extraction_note": "Optional — one sentence on anything unusual about the extraction"
  },
  "ideas": [ ... ]
}
```

**Book ID conventions:** `<short-title>-<last-name>-<year>`, all lowercase, hyphens. Examples: `mind-over-markets-dalton-2013`, `on-character-mcchrystal-2025`, `broken-money-alden-2023`.

### Step 6: Save and present

Save to `/mnt/user-data/outputs/<book-id>.json` and present the file. Do not save it in subdirectories — the user will drop it into their `idea_bank/` folder themselves.

### Step 7: Summarize

Tell the user:
- The book ID
- Themes assigned
- Idea count
- Anything unusual you skipped or flagged
- Any schema changes needed (e.g., "this book needs a new theme")

Keep this to 5–8 lines. Don't recap the book.

## Quality bar — check these before saving

1. **No glazing in the entries.** "This is a profound insight about leadership" is not a headline. "Convictions without discipline are just opinions" is.
2. **Headlines are declarative, not gerund-y.** "Embracing hardship builds capacity" is worse than "Embrace the suck." The former hedges; the latter commits.
3. **`author_example` is from the book.** If you invented it, you did the skill wrong. Go back and find the real one.
4. **`actionable_insight` is not a restatement of the principle.** If the principle is "trade the chart you're given, not the one you expected," the insight is "before placing a trade, write down one sentence describing what the market is doing right now. If you can't, don't trade." The first is a belief; the second is a behavior.
5. **No duplicates.** If two ideas restate each other, merge them or drop the weaker one.
6. **IDs are sequential and match the prefix.** `mom-001, mom-002, …`, not `mom-1, mom-003, mom-42`.

## References

- `references/schema.md` — Full JSON schema with every field documented
- `references/examples.md` — Worked examples of good and bad idea entries from real extractions
- `references/theme-guide.md` — Decision tree for tagging ambiguous books

Read the reference that matters for the specific question you're facing. Don't read them all upfront — they exist for disambiguation, not onboarding.
