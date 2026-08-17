# exp-068 — where does the real champion actually sit vs. the corrected floor? — result

**Outcome.** The "reopen the family, big headroom" framing from 066/067
was premature. Real ticks/harvest plateaus around 1070-1220, not
anywhere near the corrected 622 floor — nor the old 815 one. Memory
saturates fast (~cycle 300 of 900) but a ~17% reroll-exhaustion tail
persists at full maturity and dominates the real cost.

**Numbers.**

```
WINDOW_END 150   TICKS_PER_HARVEST_THIS_WINDOW 1446.39   MEMORY_SIZE 17   HIST [27,33,24,14,8,44]
WINDOW_END 300   TICKS_PER_HARVEST_THIS_WINDOW 1161.69   MEMORY_SIZE 23   HIST [74,71,42,27,17,69]
WINDOW_END 450   TICKS_PER_HARVEST_THIS_WINDOW 1107.33   MEMORY_SIZE 23   HIST [123,116,53,40,26,92]
WINDOW_END 600   TICKS_PER_HARVEST_THIS_WINDOW 1220.81   MEMORY_SIZE 23   HIST [167,142,78,52,40,121]
WINDOW_END 750   TICKS_PER_HARVEST_THIS_WINDOW 1106.33   MEMORY_SIZE 24   HIST [214,177,101,69,48,141]
WINDOW_END 900   TICKS_PER_HARVEST_THIS_WINDOW 1067.60   MEMORY_SIZE 24   HIST [260,216,121,87,61,155]

CYCLES 900   ELAPSED_TICKS 1066526   TICKS_PER_HARVEST 1185.03
```

Memory caps at 23-24 entries by cycle 300 and never grows further — the
companion-request diamond (distance ≤3) only covers ~25 distinct
positions, so this drone's memory is essentially saturated for the
remaining ~600 cycles, well before the run ends. That rules out "still
warming up" as the explanation for the plateau — cycles 300-900 *are*
the steady state, and it doesn't approach the floor.

At cycle 900 (cumulative), the histogram `[260,216,121,87,61,155]` sums
to 900: 28.9% hit on the very first draw (free), but **17.2% exhaust all
5 rerolls with no match**, even at full memory maturity — noticeably
higher than the ~8.8% a naive independent-draw model at p=1/3 predicts
((2/3)^6). Every one of those exhausted cycles falls through to a real
walk next cycle (200-1200 ticks depending on distance) — a structural
tax the operation-level floor math never accounted for.

**Verdict.** 066/067's operation-cost correction (207, not 400) is
real and confirmed twice over — but it was never the dominant term.
The dominant term is the exhaustion tail's walk cost, which the "622
floor" treated as fully avoidable in the idealized case and which in
practice isn't. This measurement should have come *before* declaring
the family reopened with "real room to spare" — that framing in
`queue.md`/`record.json`'s 066 note overclaimed and needs walking back.
The corrected operation costs stand; the "big headroom" conclusion
built on top of them does not, at least not for REROLL_LIMIT tuning
alone. If there's a real lever left, it's reducing the exhaustion rate
or its fallback cost specifically (e.g. remembering the *cheapest*
seen-but-unmatched option across the reroll chase instead of walking to
whatever was drawn last) — not simply retuning the limit, which
058/059 already bracketed under these same real costs. No champion
change from this measurement alone.
