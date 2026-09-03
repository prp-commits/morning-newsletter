# Schema Reference

## Current schema version: 0.3

Version 0.3 adds the `actionable_insight` field for ideas tagged `trading` or `leadership`. Older extractions on 0.2 remain valid — the sampler tolerates missing `actionable_insight`.

## Full template

```json
{
  "schema_version": "0.3",
  "book": {
    "id": "string — <short-title>-<last-name>-<year>, lowercase hyphenated",
    "title": "string — full main title",
    "subtitle": "string — optional",
    "authors": ["string — full names in the order credited"],
    "year": 2023,
    "edition": "string — optional, only if notable (e.g., 'Updated Edition')",
    "themes": ["array of themes this book covers"],
    "source_filename": "string — exact filename from /mnt/user-data/uploads/",
    "extracted_at": "YYYY-MM-DD",
    "word_count_estimate": 75000,
    "extraction_note": "string — optional, one sentence on anything unusual"
  },
  "ideas": [
    {
      "id": "string — <book-prefix>-NNN, zero-padded 3 digits",
      "headline": "string — one sentence, declarative",
      "principle": "string — 2-4 sentences, the idea in plain language",
      "author_example": "string — 2-4 sentences, from the book",
      "actionable_insight": "string — required for trading/leadership, 2-3 sentences",
      "themes": ["subset of book.themes"],
      "chapter": "string — chapter title or number",
      "section": "string — optional"
    }
  ]
}
```

## Valid themes (fixed set)

- `trading`
- `leadership`
- `economics`
- `mental_models`
- `philosophy`
- `parenting` — actionable register; maps to the Sunday email only (not the Saturday "favorite" rotation)

Do not invent new themes. If the book doesn't fit, flag it to the user. Do not silently coerce.

## ID conventions

**Book ID:** `<short-title>-<last-name>-<year>`. Short title = first 2-4 significant words of the title, no articles.

Examples:
- `Mind Over Markets` by Dalton (2013) → `mind-over-markets-dalton-2013`
- `The Bitcoin Standard` by Ammous (2018) → `bitcoin-standard-ammous-2018` (drop "The")
- `Gradually, Then Suddenly` by Lewis (2023) → `gradually-then-suddenly-lewis-2023`

**Idea ID prefix:** First letters of the short title, or the most memorable word.

Examples:
- Mind Over Markets → `mom-001`, `mom-002`, …
- On Character → `char-001`, `char-002`, …
- The Code, The Evaluation, The Protocols → `code-001`, …
- The Bitcoin Standard → `bitcoin-001`, …
- Broken Money → `broken-001`, …
- Gradually, Then Suddenly → `gts-001`, …

Zero-pad to 3 digits. Never skip or reuse.

## Field constraints

### `headline`
- One sentence. No compound sentences joined by "and" unless unavoidable.
- Declarative. "Markets auction toward the price where two-sided trade can occur" not "How markets auction."
- No marketing voice. "The surprising truth about X" fails.
- Ideally 6–14 words.

### `principle`
- 2–4 sentences. Three is the sweet spot.
- Written so someone who never read the book can understand it.
- No in-book references like "as the author argues in chapter 4."
- Present tense.

### `author_example`
- From the book. This is non-negotiable. If the book's examples are thin, extract fewer ideas rather than invent examples.
- 2–4 sentences.
- Specific: names, numbers, dates when the book provides them.
- If the "example" is really an analogy the author uses, that's fine — label it clearly.

### `actionable_insight`
- Required for ideas tagged `trading`, `leadership`, or `parenting` — those are the actionable-register themes.
- Optional (and usually omitted) for `economics`, `mental_models`, `philosophy` — those are conceptual themes.
- Note: a parenting book's ideas are commonly tagged with a companion theme too (e.g. `["parenting", "philosophy"]`). Because `parenting` is present, include the `actionable_insight` even when the companion is conceptual.
- 2–3 sentences.
- A behavior, not a belief. The test: could the reader do this (or decide not to do this) today or this week?
- Not a restatement of the principle. If the principle says "X is good," the insight should not say "do X" — it should say "specifically, here's what doing X looks like in practice."

### `themes`
- Subset of the book's themes. An idea can be narrower than the book.
- Example: a book tagged `trading` + `mental_models` can have individual ideas tagged just `mental_models` if they're general thinking tools not specific to trading.

### `chapter`
- Use the chapter title if the book has them. Fall back to number if untitled.
- For books without clear chapters (some business books use "Parts" or "Sections"), use the structural label the book uses.

## Complete example entry (trading, v0.3)

```json
{
  "id": "mom-012",
  "headline": "A narrow base gets knocked over",
  "principle": "The wider the initial balance (first hour's range), the harder it is for later participants to overwhelm it. A narrow opening range is structurally fragile and likely to see range extension.",
  "author_example": "Like the base of a lamp — the narrower the base, the easier the lamp tips over. Trend days and Double-Distribution Trend days both start with narrow initial balances that later get blown through by other-timeframe participants.",
  "actionable_insight": "When the first hour's range is unusually tight, expect range extension rather than fading the edges. Trade with the break of the initial balance rather than trying to sell the high or buy the low, because the tight range signals an under-developed auction that will expand.",
  "themes": ["trading"],
  "chapter": "Chapter 3: Advanced Beginner",
  "section": "Initial Balance"
}
```

## Complete example entry (conceptual, v0.3)

```json
{
  "id": "char-007",
  "headline": "Convictions without discipline are just opinions",
  "principle": "Beliefs that don't translate into action are inert. The gap between what people believe and what they do is closed entirely by self-discipline — the will to consistently do what you believe is right. Without it, every conviction is just talk.",
  "author_example": "McChrystal was nearly expelled from West Point for disciplinary infractions in his first two years, despite knowing exactly what was expected. He had the convictions; he lacked the discipline to align his actions with them.",
  "themes": ["leadership", "mental_models"],
  "chapter": "Self-Discipline"
}
```

Note: this entry has `leadership` in its themes, so it *should* have an `actionable_insight` — the example above shows what a v0.2 entry looks like for reference. When extracting new ideas tagged `leadership`, always include `actionable_insight`.
