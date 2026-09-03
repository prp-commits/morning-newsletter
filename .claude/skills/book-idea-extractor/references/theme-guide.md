# Theme Tagging Guide

Use this when the book's theme is ambiguous or when you're tempted to assign too many themes.

## The six themes

1. **`trading`** — market behavior, execution, psychology in a trading context, strategy design
2. **`leadership`** — leading people, making decisions under uncertainty, team dynamics, communication
3. **`economics`** — money, monetary systems, incentives, personal finance, macro, capital allocation
4. **`mental_models`** — thinking tools, cognition, reasoning, decision-making frameworks (general-purpose)
5. **`philosophy`** — character, meaning, ethics, virtue, how to live, values
6. **`parenting`** — raising kids, family, the parent-child relationship, presence, discipline, character formation in children

`parenting` is a **domain theme** (like `trading`): it anchors a book rather than describing a transferable tool, and it usually pairs with 1–2 companions from `leadership`, `mental_models`, or `philosophy`. It maps to the newsletter's single **Sunday** email only (not the Saturday "favorite" rotation) and is an **actionable** register — every parenting-tagged idea carries an `actionable_insight`.

## Rules of thumb

**Err toward fewer themes.** A book tagged with 4+ themes is almost always a book you didn't read carefully. Three is the effective cap for concept-driven books. A **domain theme** that anchors the whole book (`trading`, `parenting`) may occasionally justify a fourth tag when the companion themes are genuinely central and not merely mentioned — e.g. *The Daily Dad* is `parenting` + `philosophy` + `mental_models` + `leadership` because it's a Stoic parenting book that draws real, sustained material from all three. Still interrogate each companion; the default remains three.

**`mental_models` is not a catchall.** If every book gets tagged `mental_models`, the theme stops meaning anything. Only tag `mental_models` when the book's *primary contribution* is a thinking tool or framework — not when it happens to mention one.

**`philosophy` is for character and values, not for anything thoughtful.** A business book that quotes Seneca once is not a philosophy book.

## Worked tagging decisions

### Mind Over Markets (Dalton)
- Primary: trading — entire book is about reading markets
- Secondary: mental_models — the Market Profile framework is genuinely a thinking tool
- NOT leadership, economics, or philosophy
- **Final: `["trading", "mental_models"]`**

### On Character (McChrystal)
- Primary: leadership — McChrystal is writing as a leader to leaders
- Secondary: mental_models — many chapters teach a transferable thinking tool (e.g., "embrace the suck")
- Borderline: philosophy — the book is *about* character but frames it operationally, not philosophically
- **Final: `["leadership", "mental_models"]`** — skip philosophy because the treatment is practical, not ethical-theoretical

### The Bitcoin Standard (Ammous)
- Primary: economics — the book is a monetary history argument
- Secondary: mental_models — time preference, stock-to-flow are transferable frameworks
- NOT trading, leadership, or philosophy (though Ammous touches on time preference as a life principle)
- **Final: `["economics", "mental_models"]`**

### Principles of Economics (Ammous)
- Primary: economics
- **Final: `["economics"]`** — it's a textbook-structured argument. Single theme.

### The Gap and The Gain (Sullivan/Hardy)
- Primary: mental_models — the gap/gain framework is the entire book
- Borderline: philosophy — the framework touches on life satisfaction
- **Final: `["mental_models"]`** — don't double-tag; the gap/gain is a thinking tool, not a philosophical position

### Reset (Heath)
- Primary: mental_models — change/leverage framework
- Secondary: leadership — the book is written for managers/leaders
- **Final: `["mental_models", "leadership"]`**

### Trillion Dollar Coach
- Primary: leadership — Bill Campbell's playbook
- **Final: `["leadership"]`**

### Leadership: In Turbulent Times (Goodwin)
- Primary: leadership — four presidents as case studies
- Borderline: philosophy — character-heavy
- **Final: `["leadership"]`** — single theme is fine. The book is about leadership practice, not ethics.

### Mindful Trading (Howell)
- Primary: trading — trading psychology
- Secondary: mental_models — emotional regulation frameworks
- **Final: `["trading", "mental_models"]`**

### Mindware (Nisbett)
- Primary: mental_models — entire book is thinking tools
- **Final: `["mental_models"]`**

### Hunt, Gather, Parent (Doucleff) / How to Raise Successful People (Wojcicki)
- Primary: parenting — both are hands-on parenting method books
- Secondary: leadership (a parent leads a family) and mental_models (transferable frameworks for raising kids)
- **Final: `["parenting", "leadership", "mental_models"]`** — the standard shape for a practical parenting book

### The Daily Dad (Holiday)
- Primary: parenting — 366 meditations on raising kids
- Secondary: philosophy (it's explicitly Stoic — Marcus Aurelius, Seneca, Epictetus throughout), mental_models (dichotomy of control, finite vs. infinite games, le pause), leadership (parent-as-leader, Stutman's coaching, "leaders eat last")
- **Final: `["parenting", "philosophy", "mental_models", "leadership"]`** — a rare four-theme book justified by a domain anchor plus three genuinely central companions

### Broken Money (Alden)
- Primary: economics — monetary history + current system analysis
- Secondary: mental_models — the book offers conceptual frameworks for thinking about money
- **Final: `["economics"]`** or `["economics", "mental_models"]` — judgment call; lean toward single if the frameworks are tightly about money

### Gradually, Then Suddenly (Lewis)
- Primary: economics
- **Final: `["economics"]`**

### The Fiat Standard (Ammous)
- Primary: economics
- **Final: `["economics"]`**

## Books that don't fit

If a book doesn't cleanly fit any theme, stop and ask the user. Don't force-fit. Examples:

- Books on energy, infrastructure, industrial systems (e.g., Smil's *How the World Really Works*, Abraham's *The Elements of Power*) — these are systems books, not mental models in the Kahneman/Nisbett sense. Ask the user whether to add a `systems` theme or skip.
- Technical reference books (quant trading textbooks, API docs, programming manuals) — these are references, not idea sources. Usually skip.
- Pure memoir without transferable lessons — skip.

## When a book is genuinely multi-themed

A few books earn 3 themes. For example, a book that's simultaneously a trading memoir, a life philosophy, and a leadership treatise (rare). If you're tempted by 3+, interrogate each: does this theme describe what the book *teaches*, or just what it *mentions*? Only the former counts.

## The test

After tagging, ask yourself: "If someone subscribed to the newsletter expecting `<theme>` content and got an idea from this book, would they feel the tag was accurate?" If the answer is "eh, kind of," drop the theme.
