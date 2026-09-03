# Worked Examples

Read this when you're about to extract ideas and want to calibrate quality.

## Example 1: Good trading idea

**Source:** Mind Over Markets, Chapter 4

```json
{
  "id": "mom-018",
  "headline": "Trade the market that showed up, not the one you expected",
  "principle": "Traders come to the open with a pre-formed view. When the market opens differently than expected, the natural response is to wait for the market to 'come back' to the expected price. This is how expectation becomes a losing trade — the market doesn't owe you confirmation.",
  "author_example": "A trader expecting a rally watches the market gap down and open below the prior day's low. Instead of flipping short, he waits for the market to 'come back up' — which it never does. By the time he accepts the actual market, he's down multiple points on a position he never should have held.",
  "actionable_insight": "Before placing a trade, write down one sentence describing what the market is doing right now — not what you think it should do. If your actual trade plan contradicts that sentence, either change the plan or stay out. Never argue with the open.",
  "themes": ["trading"],
  "chapter": "Chapter 4: Competent"
}
```

**Why this works:**
- Headline is declarative and memorable
- Principle stands alone — no "as Dalton writes" references
- Example is specific: the trader *expects* a rally, gaps down, waits, never flips
- Actionable insight is a behavior ("write down one sentence…"), not a belief ("respect the market")
- The insight would not be extractable from the principle alone — you'd have to have thought about application

## Example 2: Bad trading idea (and how to fix it)

**Source:** same book, a lesser extraction attempt

```json
{
  "id": "mom-999",
  "headline": "Being disciplined is important in trading",
  "principle": "The author emphasizes that discipline is crucial for long-term success. Without discipline, even a good edge will fail. Traders need to follow their rules consistently.",
  "author_example": "The book describes how undisciplined traders fail over time while disciplined ones succeed.",
  "actionable_insight": "Be disciplined in your trading. Follow your rules every day.",
  "themes": ["trading"],
  "chapter": "Various"
}
```

**Why this fails:**
- Headline is a topic, not an idea. Every trading book says this.
- Principle references "the author" — a skill leak that shows the extraction is thin
- Example is a paraphrase of a generic claim, not a concrete case from the book
- Actionable insight restates the principle ("be disciplined" = "discipline is important")
- Chapter is "Various" — means the extractor didn't actually find where the idea lives
- Could be written by anyone who'd never read the book

**Fix:** either find a specific, concrete treatment of discipline in the book (a named trader, a named failure, a specific rule) or drop the idea. If the book really only offers "discipline is important" at this level, that's a book-level claim, not a bank-worthy idea.

## Example 3: Good conceptual idea (no actionable_insight needed)

**Source:** On Character, McChrystal

```json
{
  "id": "char-012",
  "headline": "Embrace the suck",
  "principle": "When hardship is unavoidable, the discipline of choosing to find good in it is itself protective. Steeling yourself against adversity — and refusing to be discouraged by even significant setbacks — builds capacity. Forcing yourself to act like you value something you don't can, over time, convert the feeling.",
  "author_example": "McChrystal describes Ranger school: eight weeks of starvation, cold, and exhaustion designed specifically to break people. The students who survived weren't those who minded it least — they were those who consciously decided to find meaning in the misery, and who carried that disposition into every subsequent hard assignment.",
  "actionable_insight": "When you hit a day you didn't want — a painful conversation, a frustrating project, a long-delayed task — don't negotiate with yourself about whether to do it. Start. The willingness to begin before feeling ready is the entire skill.",
  "themes": ["leadership", "mental_models"],
  "chapter": "Embrace the Suck"
}
```

**Why this works:**
- Headline uses the author's own memorable phrase — fine when it's distinctive
- Principle generalizes beyond Ranger school
- Example is specific and from the book
- Actionable insight (included because `leadership` is in themes) converts the principle into a behavior: "start before ready"
- Multi-themed (leadership + mental_models) because it's a character claim *and* a general thinking tool

## Example 4: When to split vs. merge

Sometimes two passages in the same chapter sound like two ideas but are really one. Sometimes one long passage contains two separable ideas.

**Merge when:**
- Both passages make the same claim with different examples → merge into one idea, pick the stronger example
- One is a corollary of the other → the weaker stands alone badly

**Split when:**
- The "idea" contains a belief *and* a behavior that could exist independently
- A reader could apply one without the other

If you're unsure, split. A sampler can always skip ideas; it can't unmix merged ones.

## Example 5: Books with thin examples

Some books (especially Ammous, some economics books) argue principles with logic rather than stories. The `author_example` field can be an analogy or a worked scenario from the book — it doesn't have to be a narrative. Label it honestly:

```json
{
  "author_example": "Ammous uses the analogy of a car dealership to explain the difference between flow and stock: demand for cars is flow (cars sold per year), but the relevant variable for car prices is stock (total cars in circulation). Money behaves the same way, and most monetary thinking confuses the two."
}
```

What's not acceptable is inventing an example the book doesn't contain.

## Self-check before saving

Before you write the file, re-read your first and last ideas with fresh eyes:
- Does each headline commit to a specific claim?
- Could a smart reader skim just the headlines and get value?
- Are there any ideas that could have been written without reading the book?

If yes to the last question, drop them.
